#!/usr/bin/env python3
"""
⚡ Fast Server-Side Transfer of DeepSeek-R1 (700 GB) to NadevA23/Kronumos-Aion
=============================================================================
Performs direct server-side Git LFS pointer duplication on Hugging Face backend.
Zero bytes downloaded to local machine. Takes ~8-10 minutes for all 163 shards.
"""

import os
import sys
import time
from huggingface_hub import HfApi

def main():
    token = None
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                if line.startswith("HF_TOKEN="):
                    token = line.split("=", 1)[1].strip()
    if not token:
        token = os.environ.get("HF_TOKEN")

    if not token:
        print("❌ Error: HF_TOKEN not found!")
        sys.exit(1)

    api = HfApi(token=token)
    src_repo = "deepseek-ai/DeepSeek-R1"
    dst_repo = "NadevA23/Kronumos-Aion"

    print(f"🚀 Initializing Server-Side Transfer: {src_repo} -> {dst_repo}...")
    
    # 1. Fetch file list
    src_files = api.list_repo_files(src_repo)
    safetensors_shards = sorted([f for f in src_files if f.endswith(".safetensors")])
    total_shards = len(safetensors_shards)
    print(f"📦 Found {total_shards} safetensors shards (~700 GB total).")

    # 2. Check existing files in destination
    dst_files = set(api.list_repo_files(dst_repo))
    print(f"📁 Destination currently has {len(dst_files)} files.")

    # 3. Transfer missing shards
    t_start = time.time()
    for idx, shard in enumerate(safetensors_shards):
        if shard in dst_files:
            continue
        
        t0 = time.time()
        print(f"[{idx+1}/{total_shards}] ⚡ Copying {shard} server-side...", flush=True)
        try:
            api.copy_files(
                source=f"hf://{src_repo}/{shard}",
                destination=f"hf://{dst_repo}/{shard}"
            )
            elapsed = round(time.time() - t0, 2)
            print(f"    ↳ Done in {elapsed}s", flush=True)
        except Exception as e:
            print(f"    ⚠️ Warning on {shard}: {e}. Retrying once...", flush=True)
            time.sleep(2)
            try:
                api.copy_files(
                    source=f"hf://{src_repo}/{shard}",
                    destination=f"hf://{dst_repo}/{shard}"
                )
                print(f"    ↳ Retry successful!", flush=True)
            except Exception as e2:
                print(f"    ❌ Failed {shard}: {e2}", flush=True)

    total_time = round((time.time() - t_start) / 60, 2)
    print("=" * 60)
    print(f"🎉 TRANSFER COMPLETE! All shards of DeepSeek-R1 are now in {dst_repo}!")
    print(f"⏱️ Total Time: {total_time} minutes.")
    print(f"🌐 View Repo: https://huggingface.co/{dst_repo}")
    print("=" * 60)

if __name__ == "__main__":
    main()
