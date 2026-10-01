#!/usr/bin/env python3
"""
⚡ Kronumos Aion — Single-Commit Server-Side SafeTensors Shard Transfer
========================================================================
Transfers the remaining 48 safetensors shards (116 to 163) from deepseek-ai/DeepSeek-R1
to NadevA23/Kronumos-Aion in a SINGLE commit using CommitOperationCopy.

This consumes only 1 commit quota out of the 128 commits/hour Hugging Face limit!
"""

import os
import sys
from huggingface_hub import HfApi, CommitOperationCopy

def get_token():
    with open('.env') as f:
        for line in f:
            if line.startswith('HF_TOKEN='):
                return line.strip().split('=', 1)[1]
    return os.environ.get("HF_TOKEN", "")

TOKEN = get_token()
if not TOKEN:
    print("❌ Error: HF_TOKEN not found!")
    sys.exit(1)

api = HfApi(token=TOKEN)
SRC_REPO = "deepseek-ai/DeepSeek-R1"
DEST_REPO = "NadevA23/Kronumos-Aion"

def main():
    print("🔍 Fetching current files in Kronumos-Aion...")
    existing_files = set(api.list_repo_files(repo_id=DEST_REPO))
    print(f"Total existing files: {len(existing_files)}")

    operations = []
    for i in range(1, 164):
        shard_name = f"model-{i:05d}-of-00163.safetensors"
        if shard_name not in existing_files:
            operations.append(
                CommitOperationCopy(
                    src_repo_id=SRC_REPO,
                    src_repo_type="model",
                    src_path_in_repo=shard_name,
                    path_in_repo=shard_name
                )
            )

    print(f"📦 Total missing shards to transfer: {len(operations)}")
    if not operations:
        print("🎉 All 163 shards are already present in Kronumos-Aion!")
        return

    print("🚀 Committing all missing shards in a SINGLE commit...")
    try:
        commit_info = api.create_commit(
            repo_id=DEST_REPO,
            repo_type="model",
            operations=operations,
            commit_message=f"Transfer {len(operations)} remaining safetensors shards from {SRC_REPO}"
        )
        print(f"🎉 SUKSES! All {len(operations)} shards copied in single commit: {commit_info.commit_id}")
    except Exception as e:
        print(f"❌ Commit failed (if rate limit 429, wait for the window to reset): {e}")

if __name__ == "__main__":
    main()
