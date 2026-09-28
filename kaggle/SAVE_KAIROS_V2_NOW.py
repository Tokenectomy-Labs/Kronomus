import os
import glob
import math

# -------------------------------------------------------------
# 1. Konfigurasi Token & Repositori Hugging Face
# -------------------------------------------------------------
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    try:
        from kaggle_secrets import UserSecretsClient
        HF_TOKEN = UserSecretsClient().get_secret("HF_TOKEN")
    except Exception:
        HF_TOKEN = ""

HUB_MODEL_ID = "NadevA23/Kronumos-Kairos-v2"
OUTPUT_DIR = "./kronumos_kairos_v2_lora"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 2. Dapatkan Objek Model & Tokenizer
# -------------------------------------------------------------
active_model = globals().get("model")
active_tokenizer = globals().get("tokenizer")

if active_model is not None and active_tokenizer is not None:
    print("⚡ Menggunakan bobot model yang sudah aktif di RAM GPU kernel.")
    model = active_model
    tokenizer = active_tokenizer
else:
    print("📦 Model tidak terdeteksi di global scope. Mencari checkpoint di disk...")
    from unsloth import FastLanguageModel

    checkpoints = sorted(
        glob.glob(os.path.join(OUTPUT_DIR, "checkpoint-*")),
        key=os.path.getmtime,
        reverse=True
    )
    if not checkpoints:
        checkpoints = sorted(
            glob.glob("./checkpoint-*") + glob.glob("/kaggle/working/**/checkpoint-*", recursive=True),
            key=os.path.getmtime,
            reverse=True
        )

    if checkpoints:
        best_ckpt = checkpoints[0]
        print(f"🎯 Memuat checkpoint terbaru dari disk: {best_ckpt}")
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=best_ckpt,
            max_seq_length=2048,
            load_in_4bit=True,
        )
    else:
        print(f"⚠️ Checkpoint folder belum ditemukan, memuat dari {OUTPUT_DIR}...")
        model, tokenizer = FastLanguageModel.from_pretrained(
            model_name=OUTPUT_DIR,
            max_seq_length=2048,
            load_in_4bit=True,
        )

# -------------------------------------------------------------
# 3. Simpan LoRA Adapter & Tokenizer Resmi
# -------------------------------------------------------------
print(f"💾 Menyimpan LoRA Adapter final ke {OUTPUT_DIR}...")
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"✅ SUKSES! LoRA Adapter Kronumos Kairos v2 tersimpan rapi di {OUTPUT_DIR}")

# -------------------------------------------------------------
# 4. Upload ke Hugging Face jika HF_TOKEN Tersedia
# -------------------------------------------------------------
if HF_TOKEN:
    print(f"\n🚀 [1/2] Mengunggah 16-bit merged model ke https://huggingface.co/{HUB_MODEL_ID}...")
    try:
        model.push_to_hub_merged(
            HUB_MODEL_ID,
            tokenizer,
            save_method="merged_16bit",
            token=HF_TOKEN
        )
        print("✅ Model 16-bit berhasil diunggah ke Hugging Face!")
    except Exception as e:
        print(f"⚠️ Gagal push 16-bit merged model: {e}")

    print(f"\n📦 [2/2] Mengunggah GGUF (q4_k_m) ke https://huggingface.co/{HUB_MODEL_ID}-GGUF...")
    try:
        model.push_to_hub_gguf(
            f"{HUB_MODEL_ID}-GGUF",
            tokenizer,
            quantization_method="q4_k_m",
            token=HF_TOKEN
        )
        print("✅ Model GGUF berhasil diunggah ke Hugging Face!")
    except Exception as e:
        print(f"⚠️ Gagal push GGUF model: {e}")

    print("\n" + "=" * 60)
    print("🎉 KRONUMOS KAIROS v2 SUDAH RESMI PUBLIK DI HUGGING FACE!")
    print(f"🔗 16-bit Model : https://huggingface.co/{HUB_MODEL_ID}")
    print(f"🔗 GGUF Model   : https://huggingface.co/{HUB_MODEL_ID}-GGUF")
    print("=" * 60)
else:
    print("\nℹ️ HF_TOKEN tidak diset. Model tersimpan secara lokal di Kaggle.")
    print("🚀 Siap lanjut ke tahap eksekusi evaluasi SWE-bench 500 instance!")
