#!/usr/bin/env python3
"""
⚡ Kronumos 14B — Automatic Hugging Face Hub Uploader
====================================================
Uploads the compiled GGUF Q4_K_M binary (and optional 16-bit merged weights)
to Hugging Face Hub under the NadevA23 namespace.

Usage in Google Colab:
  !python3 scripts/upload_to_hf.py
"""

import os
import sys

# 1. Resolve HF Token automatically from Colab Secrets, env, or cache
HF_TOKEN = ""
try:
    from google.colab import userdata
    HF_TOKEN = userdata.get("HF_TOKEN")
except Exception:
    pass

if not HF_TOKEN:
    HF_TOKEN = os.environ.get("HF_TOKEN", "")

if not HF_TOKEN:
    token_path = os.path.expanduser("~/.cache/huggingface/token")
    if os.path.exists(token_path):
        with open(token_path, "r", encoding="utf-8") as f:
            HF_TOKEN = f.read().strip()

if not HF_TOKEN:
    try:
        from getpass import getpass
        HF_TOKEN = getpass("Masukkan Hugging Face Write Token: ")
    except Exception:
        print("❌ Error: HF_TOKEN tidak ditemukan di Colab Secrets atau Environment!")
        sys.exit(1)

try:
    from huggingface_hub import HfApi, login
except ImportError:
    os.system("pip install -q huggingface_hub")
    from huggingface_hub import HfApi, login

print("🔑 Mengotentikasi ke Hugging Face...")
login(token=HF_TOKEN)
api = HfApi(token=HF_TOKEN)

user_info = api.whoami()
username = user_info.get("name", "NadevA23")
print(f"👤 Berhasil login sebagai: {username}")

# 2. Upload GGUF Q4_K_M Binary (Target utama untuk Ollama)
GGUF_DIR = "./kronumos_14b_gguf"
GGUF_REPO = f"{username}/Kronumos-14B-Kairos-GGUF"

if os.path.exists(GGUF_DIR) and os.listdir(GGUF_DIR):
    print(f"\n📦 Membuat dan mengunggah model GGUF ke https://huggingface.co/{GGUF_REPO}...")
    api.create_repo(repo_id=GGUF_REPO, repo_type="model", exist_ok=True)
    api.upload_folder(
        folder_path=GGUF_DIR,
        repo_id=GGUF_REPO,
        repo_type="model",
    )
    print(f"🎉 SUKSES! Model GGUF 14B resmi tayang di: https://huggingface.co/{GGUF_REPO}")
else:
    print(f"⚠️ Folder {GGUF_DIR} kosong atau belum selesai diekspor di Cell 8.")

# 3. Upload 16-bit Merged Safetensors (Opsional jika folder ada)
MERGED_DIR = "./kronumos_14b_kairos_merged_16bit"
MERGED_REPO = f"{username}/Kronumos-14B-Kairos"

if os.path.exists(MERGED_DIR) and os.listdir(MERGED_DIR):
    print(f"\n🚀 Mengunggah bobot 16-bit ke https://huggingface.co/{MERGED_REPO}...")
    api.create_repo(repo_id=MERGED_REPO, repo_type="model", exist_ok=True)
    api.upload_folder(
        folder_path=MERGED_DIR,
        repo_id=MERGED_REPO,
        repo_type="model",
    )
    print(f"🎉 SUKSES! Model 16-bit resmi tayang di: https://huggingface.co/{MERGED_REPO}")

print("\n✨ Seluruh proses rilis ke Hugging Face selesai!")
