import os

# -------------------------------------------------------------
# 0. Konfigurasi Lingkungan GPU & Bypass Multiprocessing Pickle Error
# -------------------------------------------------------------
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Kunci ke GPU 0 tunggal agar bebas dari accelerate multi-GPU hook
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ["UNSLOTH_DATASET_NUM_PROC"] = "0"  # Nonaktifkan multiprocessing Unsloth (mencegah dill pickle error di Jupyter)

import glob
import json
import math
import inspect
import torch

from datasets import Dataset
from trl import SFTTrainer
from transformers import TrainingArguments
from unsloth import FastLanguageModel, is_bfloat16_supported
from unsloth.chat_templates import get_chat_template, train_on_responses_only

# Interceptor agar Dataset.map SELALU berjalan single-process di main thread.
# CATATAN TEKNIS: Di datasets >= 4.1, `num_proc=1` tetap membuat mp.Pool(1) yang memicu dill pickle error!
# Hanya `num_proc=None` yang mengeksekusi langsung di proses utama tanpa membuat worker pool.
while getattr(Dataset.map, "__name__", "") == "_safe_single_proc_map":
    if hasattr(Dataset.map, "_original_map"):
        Dataset.map = Dataset.map._original_map
    else:
        break

_orig_map = Dataset.map
def _safe_single_proc_map(self, *args, **kwargs):
    kwargs["num_proc"] = None
    if len(args) >= 16:
        args = list(args)
        args[15] = None
        args = tuple(args)
    return _orig_map(self, *args, **kwargs)
_safe_single_proc_map._original_map = _orig_map
Dataset.map = _safe_single_proc_map

# Interceptor PyTorch GradScaler agar mendukung unscaling BFloat16 di GPU T4
# Mencegah crash NotImplementedError: "_amp_foreach_non_finite_check_and_unscale_cuda" not implemented for 'BFloat16'
if hasattr(torch, "_amp_foreach_non_finite_check_and_unscale_"):
    _orig_amp_unscale = torch._amp_foreach_non_finite_check_and_unscale_
    def _safe_amp_unscale(grads, found_inf, inv_scale):
        if grads and grads[0].dtype == torch.bfloat16:
            for g in grads:
                if torch.isinf(g).any() or torch.isnan(g).any():
                    found_inf.add_(1.0)
                g.mul_(inv_scale.to(g.device, dtype=g.dtype))
            return
        return _orig_amp_unscale(grads, found_inf, inv_scale)
    torch._amp_foreach_non_finite_check_and_unscale_ = _safe_amp_unscale

# -------------------------------------------------------------
# 1. Konfigurasi Token Hugging Face
# -------------------------------------------------------------
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    try:
        from kaggle_secrets import UserSecretsClient
        HF_TOKEN = UserSecretsClient().get_secret("HF_TOKEN")
    except Exception:
        HF_TOKEN = ""  # Masukkan token Hugging Face secara manual jika perlu

HUB_MODEL_ID = "NadevA23/Kronumos-Kairos-v2"

# -------------------------------------------------------------
# 2. Deteksi Otomatis Dataset .jsonl di /kaggle/input/ atau lokal
# -------------------------------------------------------------
train_paths = sorted(
    glob.glob("/kaggle/input/**/kairos_v2_train.jsonl", recursive=True)
    + glob.glob("dataset/kairos_v2_train.jsonl")
    + glob.glob("/kaggle/input/**/kairos_v2_master_train.jsonl", recursive=True)
    + glob.glob("/kaggle/input/**/*train*.jsonl", recursive=True)
)
val_paths = sorted(
    glob.glob("/kaggle/input/**/kairos_v2_val.jsonl", recursive=True)
    + glob.glob("dataset/kairos_v2_val.jsonl")
    + glob.glob("/kaggle/input/**/kairos_v2_master_val.jsonl", recursive=True)
    + glob.glob("/kaggle/input/**/*val*.jsonl", recursive=True)
)

if not train_paths:
    raise FileNotFoundError("❌ File training .jsonl tidak ditemukan di /kaggle/input/ atau ./dataset/!")

train_file = train_paths[0]
val_file = val_paths[0] if val_paths else None
print(f"📂 Dataset Train Terdeteksi: {train_file}")
print(f"📂 Dataset Val Terdeteksi  : {val_file}")

# -------------------------------------------------------------
# 3. Load Base Model 7B (Unsloth 4-bit NF4) & Konfigurasi LoRA
# -------------------------------------------------------------
# Dataset kita max 1,270 token. max_seq_length=2048 sangat lega dan mencegah VRAM spike/CPU offloading!
max_seq_length = 2048
print("⚡ Memuat Qwen2.5-Coder-7B-Instruct (4-bit)...")
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="Qwen/Qwen2.5-Coder-7B-Instruct",
    max_seq_length=max_seq_length,
    dtype=torch.float16,  # Wajib float16 di Nvidia T4 (Turing CC 7.5 tidak support native bfloat16)
    load_in_4bit=True,
)

model = FastLanguageModel.get_peft_model(
    model,
    r=64,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    lora_alpha=128,
    lora_dropout=0,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=42,
)

# Pastikan konfigurasi model dan semua trainable LoRA parameters bertipe float16
if hasattr(model, "config"):
    model.config.torch_dtype = torch.float16

for name, param in model.named_parameters():
    if param.requires_grad:
        param.data = param.data.to(torch.float16)

# Lepas Accelerate hooks & pastikan 100% bobot berada di GPU (mencegah error Triton cpu tensor)
try:
    from accelerate.hooks import remove_hook_from_submodules
    remove_hook_from_submodules(model)
except Exception:
    pass

for name, param in model.named_parameters():
    if param.device.type == "cpu":
        param.data = param.data.to("cuda")

for name, buf in model.named_buffers():
    if buf.device.type == "cpu":
        buf.data = buf.data.to("cuda")

tokenizer = get_chat_template(
    tokenizer,
    chat_template="qwen-2.5",
)

# -------------------------------------------------------------
# 4. Siapkan Data ChatML (Langsung Pre-Tokenized agar SFTTrainer bebas dari dill/multiprocess)
# -------------------------------------------------------------
def load_jsonl(path):
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def format_and_tokenize(data):
    all_input_ids = []
    all_attention_mask = []
    for x in data:
        if "messages" in x:
            text = tokenizer.apply_chat_template(
                x["messages"], tokenize=False, add_generation_prompt=False
            )
        elif "text" in x:
            text = x["text"]
        enc = tokenizer(text, max_length=max_seq_length, truncation=True, padding=False)
        all_input_ids.append(enc["input_ids"])
        all_attention_mask.append(enc["attention_mask"])
    return {"input_ids": all_input_ids, "attention_mask": all_attention_mask}


train_data = load_jsonl(train_file)
train_dataset = Dataset.from_dict(format_and_tokenize(train_data))
print(f"📊 Data Training Siap: {len(train_dataset)} instances (pre-tokenized).")

eval_dataset = None
if val_file:
    val_data = load_jsonl(val_file)
    eval_dataset = Dataset.from_dict(format_and_tokenize(val_data))
    print(f"📊 Data Validasi Siap: {len(eval_dataset)} instances (pre-tokenized).")

# -------------------------------------------------------------
# 5. Konfigurasi SFTTrainer dengan Single Process & Optimal VRAM
# -------------------------------------------------------------
training_args = {
    "per_device_train_batch_size": 1,      # Batch size 1 per step (hemat VRAM, tidak spike)
    "gradient_accumulation_steps": 16,     # Effective batch size = 16 (stabilitas gradien optimal)
    "warmup_ratio": 0.05,
    "num_train_epochs": 3,
    "learning_rate": 2e-4,
    "fp16": True,                          # Float16 aktif untuk GPU T4
    "bf16": False,                         # BFloat16 mati (mencegah NotImplementedError pada GradScaler)
    "logging_steps": 10,
    "optim": "paged_adamw_8bit",
    "weight_decay": 0.01,
    "lr_scheduler_type": "cosine",
    "seed": 42,
    "output_dir": "./kronumos_kairos_v2_lora",
    "report_to": "none",
    "dataset_num_proc": None,              # None = Single-process di main thread (100% bebas pickle error)
}

if eval_dataset is not None:
    training_args["per_device_eval_batch_size"] = 1
    if hasattr(TrainingArguments, "eval_strategy"):
        training_args["eval_strategy"] = "epoch"
    else:
        training_args["evaluation_strategy"] = "epoch"
    training_args["save_strategy"] = "epoch"
    training_args["load_best_model_at_end"] = True

sft_sig = inspect.signature(SFTTrainer.__init__).parameters
sft_kwargs = {
    "model": model,
    "train_dataset": train_dataset,
    "eval_dataset": eval_dataset,
}

if "processing_class" in sft_sig:
    sft_kwargs["processing_class"] = tokenizer
else:
    sft_kwargs["tokenizer"] = tokenizer

if "max_seq_length" in sft_sig:
    sft_kwargs["max_seq_length"] = max_seq_length
elif "max_length" in sft_sig:
    sft_kwargs["max_length"] = max_seq_length

if "dataset_num_proc" in sft_sig:
    sft_kwargs["dataset_num_proc"] = None

if "packing" in sft_sig:
    sft_kwargs["packing"] = False

try:
    from trl import SFTConfig
    cfg_sig = inspect.signature(SFTConfig.__init__).parameters
    cfg_dict = dict(training_args)
    if "max_seq_length" in cfg_sig and "max_seq_length" not in sft_kwargs:
        cfg_dict["max_seq_length"] = max_seq_length
    elif "max_length" in cfg_sig and "max_length" not in sft_kwargs:
        cfg_dict["max_length"] = max_seq_length
    cfg_dict["dataset_num_proc"] = None
    valid_cfg = {k: v for k, v in cfg_dict.items() if k in cfg_sig}
    sft_kwargs["args"] = SFTConfig(**valid_cfg)
except Exception:
    sft_kwargs["args"] = TrainingArguments(**training_args)

trainer = SFTTrainer(**sft_kwargs)

# Hanya latih respons assistant (masking prompt input)
trainer = train_on_responses_only(
    trainer,
    instruction_part="<|im_start|>user\n",
    response_part="<|im_start|>assistant\n",
)

# -------------------------------------------------------------
# 6. Jalankan Training & Hitung Final Eval Loss
# -------------------------------------------------------------
print("🔥 Memulai fine-tuning Kronumos Kairos v2...")
trainer.train()

if eval_dataset is not None:
    print("📊 Menghitung evaluasi final pada data validasi...")
    try:
        eval_res = trainer.evaluate()
        loss = eval_res.get("eval_loss", 0.0)
        print(f"✅ Final Validation Loss: {loss:.4f} | Perplexity: {math.exp(loss):.2f}")
    except Exception as e:
        print(f"⚠️ Evaluasi visual notebook dilewati ({e}), lanjut menyimpan model...")

# -------------------------------------------------------------
# 7. Simpan Model & Auto-Upload ke Hugging Face (16-bit & GGUF)
# -------------------------------------------------------------
output_dir = "./kronumos_kairos_v2_lora"
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)
print(f"💾 LoRA Adapter tersimpan di {output_dir}")

if HF_TOKEN:
    print(f"🚀 Mengunggah 16-bit merged model ke https://huggingface.co/{HUB_MODEL_ID}...")
    model.push_to_hub_merged(
        HUB_MODEL_ID, tokenizer, save_method="merged_16bit", token=HF_TOKEN
    )

    print(f"📦 Mengunggah GGUF (q4_k_m) ke https://huggingface.co/{HUB_MODEL_ID}-GGUF...")
    model.push_to_hub_gguf(
        f"{HUB_MODEL_ID}-GGUF", tokenizer, quantization_method="q4_k_m", token=HF_TOKEN
    )
    print("🎉 SUKSES! Model Kairos v2 sudah live dan siap digunakan!")
else:
    print("⚠️ HF_TOKEN tidak diset — model tersimpan lokal di Kaggle, lewati upload HF.")
