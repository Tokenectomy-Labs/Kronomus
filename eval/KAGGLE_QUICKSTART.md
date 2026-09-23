# 🚀 Panduan Menjalankan Kronumos Benchmark di Kaggle (Gratis & Cepat)

Panduan langkah demi langkah untuk menjalankan pengujian Kronumos di **Kaggle GPU** tanpa membebani laptop Anda:

---

## 1. Buat Kaggle Notebook Baru
1. Buka [kaggle.com/code](https://www.kaggle.com/code) dan klik **"New Notebook"**.
2. Di panel kanan (Notebook Settings):
   * **Accelerator:** Pilih **GPU T4 x2** atau **GPU P100** (100% gratis dari kuota 30 jam/minggu Kaggle).
   * **Internet:** Pastikan opsi **Internet ON** dicentang (untuk mendownload model dan dataset).

---

## 2. Install Dependensi
Di cell pertama notebook Kaggle, jalankan:
```bash
!pip install -q transformers datasets accelerate bitsandbytes
```

---

## 3. Jalankan Runner Kronumos
Di cell kedua, unduh dan jalankan script runner:
```bash
!wget -q https://raw.githubusercontent.com/daffa2555/Kronomus/main/scripts/kaggle_kronumos_runner.py
!python kaggle_kronumos_runner.py --num_samples 15 --output_dir output
```

*Script ini akan:*
1. Memuat model `NadevA23/Kronumos` ke GPU Kaggle.
2. Mengambil 15 sample issue resmi dari `princeton-nlp/SWE-bench_Verified`.
3. Menjalankan Kronumos agentic loop: diagnosa ➔ redaksi token ➔ synthesize patch.
4. Menghasilkan file `predictions.jsonl` dan `eval_metrics.json`.

---

## 4. Evaluasi Resmi di Docker GitHub Actions (0% Beban Laptop)
1. Setelah selesai, download file `predictions.jsonl` dari tab **Output** di Kaggle.
2. Masukkan / commit file `predictions.jsonl` ke repository GitHub `daffa2555/Kronomus`.
3. **GitHub Actions otomatis menyala!**
   * GitHub Actions akan menjalankan container Docker resmi Princeton SWE-bench di cloud.
   * Menjalankan test suite asli repository.
   * Menampilkan hasil scorecard terverifikasi secara publik.
