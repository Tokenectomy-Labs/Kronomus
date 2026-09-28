import os
import sys
import glob
import shutil
import zipfile
import subprocess

def main():
    print("⚡ [Kronumos Kairos v2] Mempersiapkan Runner 500 SWE-bench...")

    working_dir = "/kaggle/working" if os.path.exists("/kaggle/working") else os.path.abspath(".")
    target_runner = os.path.join(working_dir, "KAGGLE_RUNNER_500_MONOLITH.py")

    # 1. Cek apakah runner sudah ada di target
    if not os.path.exists(target_runner):
        print("🔍 Mencari file KAGGLE_RUNNER_500_MONOLITH.py di /kaggle/input/ atau subfolder...")
        found = glob.glob("/kaggle/**/KAGGLE_RUNNER_500_MONOLITH.py", recursive=True) + glob.glob("**/KAGGLE_RUNNER_500_MONOLITH.py", recursive=True)
        
        if found:
            src = found[0]
            shutil.copy(src, target_runner)
            print(f"✅ Berhasil menyalin: {src} -> {target_runner}")
        else:
            # 2. Coba ekstrak dari zip jika ada
            zips = glob.glob("/kaggle/**/*.zip", recursive=True) + glob.glob("*.zip")
            if zips:
                print(f"📦 Mengekstrak bundle dari {zips[0]} ke {working_dir}...")
                with zipfile.ZipFile(zips[0], "r") as z:
                    z.extractall(working_dir)
                print("✅ Ekstraksi zip selesai!")
            else:
                print("❌ File KAGGLE_RUNNER_500_MONOLITH.py atau file .zip tidak ditemukan.")
                print("Daftar isi direktori:")
                subprocess.run(["ls", "-la", working_dir])
                if os.path.exists("/kaggle/input"):
                    subprocess.run(["ls", "-la", "/kaggle/input"])
                sys.exit(1)

    # 3. Jalankan Runner Monolitik
    if os.path.exists(target_runner):
        print(f"\n🚀 Menjalankan Runner: {sys.executable} {target_runner}\n")
        sys.stdout.flush()
        cmd = [sys.executable, target_runner]
        subprocess.run(cmd, check=True)
    else:
        print(f"❌ Target runner {target_runner} belum ditemukan.")
        sys.exit(1)

if __name__ == "__main__":
    main()
