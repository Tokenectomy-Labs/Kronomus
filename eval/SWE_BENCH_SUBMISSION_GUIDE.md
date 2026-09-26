# 🏆 SWE-bench Verified Official Leaderboard Submission Guide

Panduan lengkap untuk mendaftarkan **Kronumos-7B** ke [Official SWE-bench Leaderboard](https://www.swebench.com/) melalui repositori [SWE-bench/experiments](https://github.com/SWE-bench/experiments).

---

## 📦 Paket Submission yang Sudah Disiapkan

Folder submission lengkap sudah dibuat di repositori ini:
`eval/submission/evaluation/verified/20260923_tokenectomy_kronumos-7b/`

Isi folder:
1. `metadata.yaml` — Informasi model, organisasi, lisensi OSS, dan DOI paper.
2. `all_preds.jsonl` — 500 prediksi lengkap untuk SWE-bench Verified.
3. `results/results.json` — Rincian hasil task yang lolos evaluasi.
4. `README.md` — Rangkuman metodologi, arsitektur Sub-Cortex, dan benchmark.
5. `logo.png` — Logo resmi Tokenectomy / Kronumos.

---

## 🚀 Langkah 1: Fork Repositori `SWE-bench/experiments`

1. Buka browser dan kunjungi: **[https://github.com/SWE-bench/experiments](https://github.com/SWE-bench/experiments)**
2. Klik tombol **Fork** di pojok kanan atas untuk membuat fork di akun GitHub kamu (`daffa2555/experiments`).

---

## 💻 Langkah 2: Clone Fork & Salin Folder Submission

Jalankan perintah berikut di terminal kamu:

```bash
# 1. Clone fork repositori experiments kamu ke folder terpisah
cd ~
git clone https://github.com/daffa2555/experiments.git swebench-experiments
cd swebench-experiments

# 2. Buat branch baru untuk submission
git checkout -b submit-kronumos-7b

# 3. Salin folder submission dari repo Kronomus kamu
cp -r "/home/nans/web anonim/eval/submission/evaluation" .

# 4. Verifikasi file yang baru disalin
git status

# 5. Commit dan push ke branch kamu
git add evaluation/verified/20260923_tokenectomy_kronumos-7b/
git commit -m "feat(evaluation): add Kronumos-7B SWE-bench Verified submission"
git push origin submit-kronumos-7b
```

---

## 📝 Langkah 3: Buka Pull Request (PR)

1. Buka halaman GitHub fork kamu: `https://github.com/daffa2555/experiments`
2. Klik tombol hijau **"Compare & pull request"**.
3. Gunakan data berikut untuk judul dan isi PR:

### Judul PR:
```text
[Verified Submission] Kronumos-7B (Tokenectomy Labs)
```

### Isi Deskripsi PR (Copy-Paste template ini):

```markdown
### Submission Summary
- **Model / System**: Kronumos-7B (Fine-tuned Qwen2.5-Coder-7B-Instruct via LoRA)
- **Sub-Cortex**: Tokenectomy (Rust M2M context surgery & POSIX diff re-anchoring)
- **Organization**: Tokenectomy Labs
- **Repository**: https://github.com/Tokenectomy-Labs/Kronomus
- **Technical Report / Preprint**: https://doi.org/10.5281/zenodo.22929676
- **Model Weights**: https://huggingface.co/NadevA23/Kronumos
- **Split**: `SWE-bench_Verified` (All 500 instances)
- **Protocol**: Blind Single-Turn (Pass@1, zero execution tools, zero hints, zero web-browsing)

---

### Submission Checklist
- [x] I have tested my submission using `swebench` evaluation harness.
- [x] This is a single-attempt (Pass@1) submission.
- [x] The agent / system did **not** use test knowledge (`PASS_TO_PASS` / `FAIL_TO_PASS` test suites).
- [x] The agent / system did **not** use the `hints_text` field.
- [x] The system did **not** use web browsing or unauthorized external solution lookup.
- [x] Prediction file `all_preds.jsonl` contains exactly 500 instances.
- [x] `metadata.yaml` and `README.md` are properly populated.
- [x] Push permissions granted to maintainers for verification.
```

---

## 🎯 Apa yang Terjadi Setelah PR Dibuka?

1. Tim maintainer SWE-bench (Princeton NLP) akan memverifikasi integritas `all_preds.jsonl`.
2. Hasil evaluasi akan di-merge ke branch `main`.
3. Nama **Kronumos-7B** dari **Tokenectomy Labs** akan resmi terpajang di leaderboard global: **[swebench.com](https://www.swebench.com/)**!
