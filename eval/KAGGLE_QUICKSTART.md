# 🚀 Kronumos Kaggle Benchmark Quickstart (Zero-Cost & Cloud-Accelerated)

Step-by-step guide to run the official Kronumos SWE-bench benchmark on **Kaggle Cloud GPUs** without local hardware strain:

---

## 1. Create a New Kaggle Notebook
1. Navigate to [kaggle.com/code](https://www.kaggle.com/code) and click **"New Notebook"**.
2. In the right-side configuration panel (**Notebook Settings**):
   * **Accelerator:** Select **GPU T4 x2** or **GPU P100** (Free from Kaggle's 30h/week quota).
   * **Internet:** Ensure **Internet ON** is enabled (required to fetch model weights and dataset splits).

---

## 2. Install Required Dependencies
In the first notebook cell, execute:
```bash
!pip install -q transformers datasets accelerate bitsandbytes
```

---

## 3. Clone and Run Kronumos Benchmark
In the second cell, fetch the runner from the official repository and launch:
```bash
!rm -rf Kronomus
!git clone https://github.com/Tokenectomy-Labs/Kronomus.git
!cp Kronomus/scripts/kaggle_kronumos_runner.py ./kaggle_kronumos_runner.py
!python kaggle_kronumos_runner.py --num_samples 500 --output_dir output
```

*The benchmark runner will:*
1. Load `NadevA23/Kronumos` (4-bit NF4 quantized) into Kaggle GPU VRAM (~5.5 GB).
2. Iterate through the official `SWE-bench/SWE-bench_Verified` dataset split.
3. Execute the full surgical agent loop: diagnosis ➔ token pruning via Tokenectomy Sub-Cortex ➔ atomic POSIX unified diff generation.
4. Output verified prediction artifacts: `output/predictions.jsonl` and `output/eval_metrics.json`.

---

## 4. Automated Verification via GitHub Actions Docker Harness
1. Once completed, download `predictions.jsonl` from Kaggle's **Output** tab.
2. Commit `predictions.jsonl` to the `Tokenectomy-Labs/Kronomus` repository.
3. **GitHub Actions Docker Testbed triggers automatically:**
   * Runs the official Princeton NLP SWE-bench evaluation harness inside isolated Docker containers.
   * Executes upstream repository test suites (`pytest`, `runtests.py`).
   * Generates a fully verifiable, reproducible resolution scorecard.
