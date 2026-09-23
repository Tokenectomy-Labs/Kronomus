# 🗺️ Product & Engineering Roadmap: Kronumos

**Codename:** `Kronumos`  
**Core Slogan:** *"You write the features. Kronumos heals the bugs."*  
**Founder:** Daffa ([@daffa2555](https://github.com/daffa2555)) — Tokenectomy Labs  
**Last Updated:** September 23, 2026  

---

## 🏁 Phase 1: The Core Foundation (COMPLETED ✅)

- [x] **Model Fine-Tuning:**
  - Base: `Qwen2.5-Coder-7B-Instruct`
  - Dataset: 1,080 multi-turn trajectories with full tool-calling discipline.
  - Final Loss: Train `0.239`, Val `0.233` (Zero Overfitting).
  - Hosted at: `NadevA23/Kronumos` (BF16) & `NadevA23/Kronumos-GGUF` (Q4_K_M, Q8_0).
- [x] **Sub-Cortex Integration:**
  - Tokenectomy Rust Engine linked directly with secret redaction (JWT, AWS, DB URLs).
  - 95.2% token bloat reduction on raw stack traces.
- [x] **First Empirical SWE-bench Lite Validation:**
  - **100%** Tool Call Emission Rate (10/10).
  - **100%** Patch Synthesis Rate (10/10).
  - **40%** Real-File Verbatim Match at base commit.
  - **70%** Full Git Delivery Rate (`branch` ➔ `commit` ➔ `open_pr`).
- [x] **CLI REPL Binary:**
  - Rust binary compiled successfully at `Tokenectomy-OSS/src/bin/kronumos.rs` (and `mend.rs`).
  - Supports `--backend cloudflare`, `--backend ollama`, and `--backend openai`.

---

## 🥊 Phase 2: The Arena — Head-to-Head Benchmark Suite (🔥 PRIORITAS #1: FIRST TEST TO RUN)

**Objective:** Membuktikan secara empiris bahwa model 7B + Rust Sub-Cortex mengungguli brute-force LLMs (Llama-3.3 70B / DeepSeek V3) dalam hal efisiensi biaya, reduksi token, latensi, dan jaminan zero dirty diffs menggunakan standar evaluasi perusahaan AI papan atas (OpenAI, Anthropic, Cognition/Devin).

- [ ] **Target Dataset & Benchmark Environment:**
  - **Primary:** `princeton-nlp/SWE-bench_Verified` (500 human-validated tasks — standard industri saat ini).
  - **Secondary/Stress-Test:** Stratified sample of 30 heavy issues dari `SWE-bench` Full (Django, Sympy, Matplotlib, Scikit-learn, Sphinx).
  - **Environment:** Isolated Docker container test harness untuk evaluasi 100% reproducible.
- [ ] **Competitor Baseline:**
  - Llama-3.3 70B & DeepSeek V3 (via Groq API / OpenRouter) tanpa Sub-Cortex (raw prompt brute-force).
- [ ] **Comprehensive Enterprise AI Metrics Suite (Metrik Lengkap Standar Lab AI):**

  #### 1. Resolution & Correctness Quality (Kualitas Solusi Kode)
  - **Resolved Rate (% Pass@1):** Persentase task di mana patch berhasil menyelesaikan bug dan seluruh test suite lolos (PASS).
  - **Fail-to-Pass (F2P) Pass Rate:** Persentase test case yang awalnya gagal (akibat bug) yang berhasil berubah menjadi hijau/sukses.
  - **Pass-to-Pass (P2P) Regression Rate:** Menjamin 100% test case yang sebelumnya lulus TIDAK rusak oleh patch baru (Zero Regression).
  - **AST Syntax Validity Rate:** Persentase patch yang valid secara sintaksis sebelum test dieksekusi (diverifikasi via Tree-sitter parser).

  #### 2. Granular Tokenomics & Economic Efficiency (Ekonomi & Token Riil)
  - **Input vs Output Token Consumption:** Rata-rata token input dan output per task (Mean, Median, p95).
  - **Peak Context Utilization:** Puncak penggunaan context window dalam 1 session sebelum mitigasi/truncation.
  - **Token Bloat Reduction Ratio:** Pengurangan token stack trace mentah vs tersaring Sub-Cortex (target: 80% – 95% reduction).
  - **Cost per Resolved Issue ($ / Resolved):** Biaya riil API per perbaikan bug yang sukses ($0 pada local Kronumos vs $$ pada competitor).

  #### 3. Agentic Loop & Trajectory Dynamics (Efisiensi Pola Agen)
  - **Average Turns to Resolve (Mean & Median):** Jumlah putaran tool-calling sebelum patch final disintesis.
  - **Exploration vs Exploitation Ratio:** Rasio langkah inspeksi/pembacaan file (`view_file`, `grep`) sebelum edit pertama dilakukan.
  - **Tool Error & Hallucination Rate:** Persentase kesalahan syntax tool, pemanggilan parameter salah, atau path file fiktif.
  - **Context Truncation / Amnesia Incident Rate:** Frekuensi hilangnya konteks akibat context window penuh.

  #### 4. Latency & Execution Speed (Kecepatan Eksekusi & UX)
  - **Time to First Token (TTFT):** Waktu respon awal inferensi.
  - **Generation Throughput (Tokens/s):** Kecepatan generasi token saat patching.
  - **Wall-Clock Time to Resolution:** Total durasi nyata dari penerimaan issue hingga PR terbuka (p50 & p90).
  - **Sub-Cortex Overhead vs LLM Inference:** Verifikasi overhead pembersihan Rust Sub-Cortex (< 5ms) berbanding durasi inferensi LLM (> 10s).

  #### 5. Safety, Workspace Hygiene & Security (Invarian Inti Kronumos)
  - **Workspace Dirty Diff Incident Rate:** Target mutlak: **0.0%**. Workspace harus kembali bersih 100% jika patch/test gagal.
  - **Secret Redaction Recall (0% Leakage):** Memastikan 100% token kredensial (JWT, AWS key, DB connection string) tersensor dari prompt.
  - **False Redaction Rate:** Memastikan tidak ada kode valid yang tidak sengaja terhapus/tersensor.

  #### 6. Statistical Rigor (Validitas Statistik)
  - **95% Confidence Interval (Wilson Score / Bootstrap):** Pelaporan hasil evaluasi menyertakan rentang error margin, bukan hanya angka mentah tunggal.
  - **Determinism & Reproducibility:** Penguncian random seed dan test harness scripts yang dapat diaudit publik.
- [ ] **Deliverable Utama:** Dokumen publik `ARENA_HEAD_TO_HEAD_SCORECARD.md` berisi komparasi head-to-head lengkap untuk rilis publik.

---

## ⚡ Phase 3: Infrastructure & Edge Gateway (Serverless Zero-Cost)

**Objective:** Give users a frictionless, zero-setup experience without requiring them to download 15GB models locally.

- [ ] **Edge Proxy (Cloudflare Workers AI):**
  - Deploy lightweight serverless Worker gateway.
  - Route user CLI requests to fast edge inference with Server-Sent Events (SSE) streaming.
  - Cloudflare AI Gateway caching for common library stack traces.
- [ ] **GCP Cloud Run Backup (Using $300 Free Credits):**
  - Spin up serverless container on Google Cloud Run for heavier multi-turn agent loops.
  - Scale-to-zero architecture (0 cost when idle).
- [ ] **NPM / Homebrew 1-Liner Packaging:**
  - Publish `npx kronumos` (lightweight binary wrapper, <15MB download).
  - `cargo install kronumos-cli`.

---

## 🚀 Phase 4: Launch & Distribution Flywheel

**Objective:** Attract developers, Tech Leads, and Open-Source maintainers without cold DMs or paid ads.

1. **The Hacker News & Reddit Launch Post:**
   - Title: *"Show HN: We gave a 7B model a Rust sub-cortex to heal bugs on Full SWE-bench (with 95% less tokens)"*
   - Target Subreddits: `r/LocalLLaMA`, `r/rust`, `r/programming`.
2. **GitHub Action Virality (`kronumos-action` / `tokenectomy-action`):**
   - Maintainers add 4 lines to `.github/workflows/ci.yml`.
   - On failing tests, Kronumos automatically investigates and opens a Pull Request:
     > *"⚡ Automated fix generated by [Kronumos](https://huggingface.co/NadevA23/Kronumos) with zero dirty diffs."*
   - Each PR acts as a high-trust billboard to developer teams.
3. **Monetization (The Cash Flow):**
   - **Community Tier:** 100% Free & Open-Weights (Run locally via Ollama / GGUF).
   - **Kronumos Pro ($29 - $39 Lifetime / Early Bird):** Hosted edge inference, unlimited automated GitHub PR fixes, private team rules via Polar.sh.

---

## 🎯 Guiding Invariants (Never Compromise)

1. **Machine-to-Machine First:** The CLI is an autonomous agent loop, not a chatty chatbot.
2. **Hardware-Grounded Truth:** Never publish simulated mocks; always back claims with reproducible benchmarks.
3. **Zero Dirty Diffs:** Roll back instantly if a compiler or test fails. Never leave user workspaces broken.
4. **Lean Finance:** Never burn private funds on idle GPU instances; scale serverless and let revenue fund dedicated infrastructure.
