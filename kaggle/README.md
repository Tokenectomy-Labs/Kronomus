# ⚡ Panduan Eksekusi Kronumos Kairos v2 di Kaggle ($0 Cost)

File ini dirancang agar kamu bisa menyalin kode per cell ke Kaggle Notebook dengan cepat dan mudah, atau mengunggah file notebook secara langsung.

Informasi Dataset:
1. Dataset Training LoRA: `dataset/kairos_v2_train.jsonl` (1.522 sample) & `dataset/kairos_v2_val.jsonl` (198 sample)
   - Sudah terkemas di dalam `kronumos_kairos_v2_kaggle.zip`.
2. Dataset Evaluasi SWE-bench: `princeton-nlp/SWE-bench_Verified` (500 instance resmi Princeton)
   - Diunduh otomatis oleh runner saat evaluasi dijalankan.

Pengaturan Awal Kaggle Notebook:
- Accelerator : GPU T4 x2 atau GPU P100 (pilih single GPU)
- Internet    : ON (Wajib Aktif)
- File Upload : Unggah `kronumos_kairos_v2_kaggle.zip` via menu Upload Data atau drag-and-drop ke Kaggle.


================================================================================
CELL 1: Install Dependencies (Unsloth GPU Acceleration)
================================================================================
Salin kode berikut ke Cell 1:

```python
# 1. Install Unsloth dan library akselerasi GPU
!pip install --no-deps "xformers<0.0.29" "trl<0.9.0" peft accelerate bitsandbytes
!pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
!pip install datasets
print("✅ Environment Unsloth & Datasets siap!")
```


================================================================================
CELL 2: Unpack Zip Bundle / Sinkronkan Kaggle Dataset
================================================================================
Salin kode berikut ke Cell 2:

```python
# 2. Ekstrak bundle zip atau sinkronkan Kaggle Dataset ke working directory
import os, glob, shutil, zipfile

# Cek 1: Jika Kaggle mengekstrak dataset otomatis ke /kaggle/input/
input_runners = glob.glob("/kaggle/input/**/KAGGLE_RUNNER_500_MONOLITH.py", recursive=True)
input_zips = (
    glob.glob("/kaggle/input/**/*.zip", recursive=True)
    + glob.glob("/kaggle/working/*.zip")
    + glob.glob("*.zip")
)

if input_runners:
    source_dir = os.path.dirname(input_runners[0])
    print(f"📦 Terdeteksi Kaggle Dataset di: {source_dir}")
    print("Menyalin seluruh file ke /kaggle/working/...")
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join("/kaggle/working", item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    print("✅ Seluruh file & dataset berhasil disinkronkan ke /kaggle/working/!")
elif input_zips:
    target_zip = input_zips[0]
    print(f"📦 Mengekstrak file zip: {target_zip}...")
    with zipfile.ZipFile(target_zip, "r") as z:
        z.extractall("/kaggle/working/")
    print("✅ Berhasil diekstrak ke /kaggle/working/!")
else:
    print("⚠️ File atau Dataset belum terdeteksi di Kaggle!")
    print("---------------------------------------------------------")
    print("CARA UPLOAD SANGAT MUDAH:")
    print("1. Di sidebar kanan Kaggle, klik menu '+ Add Input'.")
    print("2. Klik 'Upload a dataset', beri nama 'kronumos-bundle'.")
    print("3. Pilih/drag file zip dari laptop:")
    print("   /home/nans/Tokenonmix/dist/kronumos_kairos_v2_kaggle.zip")
    print("4. Klik 'Create', tunggu 10-20 detik hingga selesai.")
    print("5. Jalankan ulang Cell 2 ini!")
    print("---------------------------------------------------------")

%cd /kaggle/working
!ls -la
```


================================================================================
CELL 3: Training LoRA Qwen2.5-Coder-7B (Sub-Cortex Masked Loss)
================================================================================
Salin kode berikut ke Cell 3:

```python
# 3. Jalankan fine-tuning LoRA (~25-40 menit di GPU T4)
!python3 KAGGLE_TRAIN_SCRIPT.py
```

Catatan Teknis Cell 3:
- Melatih adapter LoRA r=64, alpha=128 pada model Qwen2.5-Coder-7B-Instruct.
- Menggunakan kuantisasi 4-bit NF4 untuk efisiensi VRAM.
- Menghitung loss hanya pada respon asisten (5-Step CoT & AST patch).
- Output model tersimpan di `./kronumos_kairos_v2_lora`.


================================================================================
CELL 4: Eksekusi 500 SWE-bench Verified Arena (Full Sub-Cortex)
================================================================================
Salin kode berikut ke Cell 4:

```python
# 4. Jalankan 500 Instance SWE-bench Verified dengan Sub-Cortex Lengkap
!python3 KAGGLE_RUNNER_500_MONOLITH.py
```

Catatan Teknis Cell 4:
- Mengunduh dataset resmi `princeton-nlp/SWE-bench_Verified` (500 instance).
- Mengaktifkan seluruh spektrum Tokenectomy Sub-Cortex:
  * Issue De-Noiser & Signal Extractor (Core Triad)
  * Procedural Cognitive Kernel (9 Domain Invariant)
  * Interlocking Causal Invariant Mesh (Tension Links & Equilibrium Vector)
  * Turn 0 Speculative Mutation Seeds
  * Dual-Key Consensus Gate (Semantic Key + Deterministic AST Key)
  * Cryptographic SHA-256 Merkle Causal Chain
  * Tokenectomy AST Enclosing Function Slicer
  * AST & Sentinel Patch Validator (Anti-slop filter)
- Checkpoint Auto-Resume: Jika sesi terputus atau timeout, cukup jalankan ulang Cell 4 ini. Runner akan langsung melanjutkan dari soal terakhir yang belum selesai!
- Output tersimpan di:
  * `./eval_output_500/predictions.jsonl` (Format resmi Princeton SWE-bench)
  * `./eval_output_500/trajectories/<instance_id>.json` (Trace multi-turn & Merkle chain)
  * `./eval_output_500/eval_metrics.json` (Metrik token & latensi)


================================================================================
CELL 5 (Opsional): Upload Model ke Hugging Face
================================================================================
Salin kode berikut ke Cell 5 jika ingin menyimpan model 16-bit atau format GGUF ke Hugging Face:

```python
# 5. Upload bobot model ke Hugging Face (opsional)
# Masukkan token HF kamu jika tidak menggunakan Kaggle Secrets:
import os
os.environ["HF_TOKEN"] = ""  # Isi HF Write Token di sini jika perlu

!python3 SAVE_AND_UPLOAD_KAIROS_V2.py
```
