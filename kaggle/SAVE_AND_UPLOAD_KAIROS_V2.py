import os

# -------------------------------------------------------------
# 1. Konfigurasi Token & Repositori Hugging Face
# -------------------------------------------------------------
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    try:
        from kaggle_secrets import UserSecretsClient
        HF_TOKEN = UserSecretsClient().get_secret("HF_TOKEN")
    except Exception:
        # Masukkan HF write token kamu di sini jika tidak menggunakan Kaggle Secrets
        HF_TOKEN = ""

HUB_MODEL_ID = "NadevA23/Kronumos-Kairos-v2"
OUTPUT_DIR = "./kronumos_kairos_v2_lora"

# -------------------------------------------------------------
# 2. Ambil Model yang Sudah Selesai Ditraining
# -------------------------------------------------------------
if "model" not in globals() or "tokenizer" not in globals():
    print("📦 Model belum ada di memori. Memuat langsung dari checkpoint-204...")
    from unsloth import FastLanguageModel
    checkpoint_path = os.path.join(OUTPUT_DIR, "checkpoint-204")
    target_load = checkpoint_path if os.path.exists(checkpoint_path) else OUTPUT_DIR
    
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=target_load,
        max_seq_length=2048,
        load_in_4bit=True,
    )
else:
    print("⚡ Menggunakan model yang sudah ada di memori aktif.")

# -------------------------------------------------------------
# 3. Simpan LoRA Adapter Final
# -------------------------------------------------------------
os.makedirs(OUTPUT_DIR, exist_ok=True)
model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)
print(f"💾 LoRA Adapter resmi tersimpan di: {OUTPUT_DIR}")

# -------------------------------------------------------------
# 4. Upload ke Hugging Face (16-bit Merged & GGUF q4_k_m)
# -------------------------------------------------------------
if HF_TOKEN:
    print(f"\n🚀 [1/2] Mengunggah 16-bit merged model ke https://huggingface.co/{HUB_MODEL_ID}...")
    model.push_to_hub_merged(
        HUB_MODEL_ID,
        tokenizer,
        save_method="merged_16bit",
        token=HF_TOKEN
    )
    print("✅ Model 16-bit berhasil diunggah!")

    print(f"\n📦 [2/2] Mengunggah GGUF (q4_k_m) ke https://huggingface.co/{HUB_MODEL_ID}-GGUF...")
    model.push_to_hub_gguf(
        f"{HUB_MODEL_ID}-GGUF",
        tokenizer,
        quantization_method="q4_k_m",
        token=HF_TOKEN
    )
    print("✅ Model GGUF q4_k_m berhasil diunggah!")

    print("\n" + "=" * 60)
    print("🎉 SELAMAT! KRONUMOS KAIROS v2 SUDAH RESMI LIVE DI HUGGING FACE!")
    print(f"🔗 16-bit Model : https://huggingface.co/{HUB_MODEL_ID}")
    print(f"🔗 GGUF Model   : https://huggingface.co/{HUB_MODEL_ID}-GGUF")
    print("=" * 60)
else:
    print("\n⚠️ HF_TOKEN tidak ditemukan!")
    print("Isi variabel HF_TOKEN di atas atau setel di Kaggle Secrets -> HF_TOKEN.")
