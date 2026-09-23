import os
import shutil
import subprocess
import sys

# 1. Masuk ke folder Kronomus (clone jika di sesi Kaggle baru)
repo_dir = "/kaggle/working/Kronomus" if os.path.exists("/kaggle/working") else os.path.abspath(".")

if os.path.exists("/kaggle/working") and not os.path.exists(repo_dir):
    print("📥 Cloning repository to /kaggle/working/Kronomus...")
    subprocess.run(["git", "clone", "https://github.com/Tokenectomy-Labs/Kronomus.git", repo_dir], check=True)

if os.path.exists(repo_dir):
    os.chdir(repo_dir)
    print(f"📂 Current working directory: {os.getcwd()}")
    try:
        subprocess.run(["git", "pull", "origin", "main"], check=False)
    except Exception as e:
        print(f"⚠️ Git pull warning: {e}")

# 2. Siapkan folder output & pastikan checkpoint 500 task kemarin terbaca
os.makedirs("output", exist_ok=True)
if not os.path.exists("output/predictions.jsonl") and os.path.exists("predictions.jsonl"):
    shutil.copy("predictions.jsonl", "output/predictions.jsonl")
    print("📋 Checkpoint 500 task kemarin berhasil dimuat ke output/predictions.jsonl!")

# 3. Jalankan runner baru (6 turn + hanya eksekusi task yang masih kosong)
cmd = [
    sys.executable,
    "scripts/kaggle_kronumos_runner.py",
    "--num_samples", "500",
    "--max_turns", "6",
    "--retry_empty"
]
print(f"🚀 Executing runner: {' '.join(cmd)}")
subprocess.run(cmd)