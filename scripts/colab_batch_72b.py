#!/usr/bin/env python3
"""
⚡ Kronumos 72B Batch Evaluator for Google Colab
=================================================
Dapat dijalankan langsung di Colab dengan:
  %run -i scripts/colab_batch_72b.py
atau via terminal:
  python scripts/colab_batch_72b.py --num_samples 5
"""

import os
import sys
import json
import time
import argparse

try:
    import torch
except ImportError:
    torch = None

try:
    from datasets import load_dataset
except ImportError:
    load_dataset = None

try:
    from scripts.kaggle_kronumos_runner import KronumosBenchmarkRunner
except ImportError:
    from kaggle_kronumos_runner import KronumosBenchmarkRunner


def run_batch():
    parser = argparse.ArgumentParser(description="Kronumos 72B Colab Batch Runner")
    parser.add_argument("--num_samples", type=int, default=5, help="Jumlah soal yang akan diuji (default: 5)")
    parser.add_argument("--max_turns", type=int, default=3, help="Maksimal turns per issue (default: 3)")
    parser.add_argument("--output_dir", type=str, default="output_colab_72b_5", help="Direktori output")
    
    # Hanya parse args jika dijalankan via CLI, abaikan argumen jupyter jika via %run
    if any(arg.startswith("--") for arg in sys.argv):
        args, _ = parser.parse_known_args()
    else:
        args = parser.parse_args([])

    os.makedirs(args.output_dir, exist_ok=True)
    pred_file = os.path.join(args.output_dir, "predictions.jsonl")
    metrics_file = os.path.join(args.output_dir, "eval_metrics.json")

    # 1. Reuse atau Inisialisasi Runner
    global runner
    if "runner" in globals() and globals()["runner"] is not None:
        active_runner = globals()["runner"]
        print("⚡ Menggunakan model 72B yang SUDAH AKTIF di VRAM GPU (0 detik reload)!")
    else:
        gh_token = os.environ.get("GITHUB_TOKEN", "")
        model_id = "unsloth/Qwen2.5-72B-Instruct-bnb-4bit"
        print(f"🚀 Menginisialisasi Kronumos 72B Runner dengan {model_id}...")
        active_runner = KronumosBenchmarkRunner(model_id=model_id, load_in_4bit=True, github_token=gh_token)
        globals()["runner"] = active_runner

    # 2. Reuse atau Muat Dataset
    global ds
    if "ds" in globals() and globals()["ds"] is not None:
        dataset = globals()["ds"]
    else:
        print("📥 Memuat princeton-nlp/SWE-bench_Verified (split=test)...")
        dataset = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")
        globals()["ds"] = dataset

    num_eval = min(args.num_samples, len(dataset))
    instances = [dataset[i] for i in range(num_eval)]
    results = []

    print(f"\n🎯 Memulai evaluasi batch {num_eval} soal SWE-bench Verified (Max turns: {args.max_turns})...\n")

    for i, inst in enumerate(instances):
        iid = inst["instance_id"]
        repo = inst.get("repo", "unknown")
        print(f"[{i+1}/{num_eval}] 🔧 Memproses: {iid} ({repo})...", flush=True)

        t0 = time.time()
        res = active_runner.solve_instance(inst, max_turns=args.max_turns)
        elapsed = round(time.time() - t0, 2)

        if torch and torch.cuda.is_available():
            torch.cuda.empty_cache()

        has_patch = bool(res.get("model_patch"))
        pred_entry = {
            "instance_id": iid,
            "model_patch": res.get("model_patch", ""),
            "model_name_or_path": "Qwen2.5-72B-Instruct"
        }

        # Simpan prediksi real-time (flush ke disk)
        with open(pred_file, "a", encoding="utf-8") as pf:
            pf.write(json.dumps(pred_entry) + "\n")

        results.append({
            "instance_id": iid,
            "repo": repo,
            "has_patch": has_patch,
            "turns": res.get("turns", 1),
            "total_tokens": res.get("total_tokens", 0),
            "latency_sec": elapsed
        })

        status_badge = "✅ PATCH VALID" if has_patch else "❌ TANPA PATCH"
        print(f"    ↳ {status_badge} | Tokens: {res.get('total_tokens', 0)} | Waktu: {elapsed}s\n", flush=True)

    # Simpan ringkasan metrik
    with open(metrics_file, "w", encoding="utf-8") as mf:
        json.dump({"summary": results}, mf, indent=2)

    valid_count = sum(1 for r in results if r["has_patch"])
    print("=" * 60)
    print(f"🎉 BATCH RUN SELESAI! {valid_count}/{num_eval} soal berhasil disintesis!")
    print(f"📁 File Prediksi: {pred_file}")
    print(f"📊 Metrik Lengkap: {metrics_file}")
    print("=" * 60)


if __name__ == "__main__":
    run_batch()
