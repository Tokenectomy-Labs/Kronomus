#!/usr/bin/env python3
"""
⚡ Kronumos Aion — Single-Commit Server-Side SafeTensors Shard Transfer & License Sync
====================================================================================
Transfers the remaining 48 safetensors shards (116 to 163) from deepseek-ai/DeepSeek-R1
to NadevA23/Kronumos-Aion, while simultaneously syncing the Dual-License README.md
and LICENSE_ENTERPRISE.md in a SINGLE ATOMIC COMMIT using CommitOperationCopy and CommitOperationAdd.

This consumes only 1 commit quota out of the 128 commits/hour Hugging Face limit!
"""

import os
import sys
from huggingface_hub import HfApi, CommitOperationCopy, CommitOperationAdd

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

README_PATH = "/home/nans/web anonim/HUGGINGFACE_KRONUMOS_AION.md"
LICENSE_PATH = "/home/nans/web anonim/LICENSE_ENTERPRISE.md"

def main():
    print("🔍 Fetching current files in Kronumos-Aion...")
    existing_files = set(api.list_repo_files(repo_id=DEST_REPO))
    print(f"Total existing files: {len(existing_files)}")

    operations = []

    # 1. Add remaining SafeTensors shards (server-side copy)
    missing_shards = 0
    for i in range(1, 164):
        shard_name = f"model-{i:05d}-of-000163.safetensors"
        if shard_name not in existing_files:
            operations.append(
                CommitOperationCopy(
                    src_repo_id=SRC_REPO,
                    src_repo_type="model",
                    src_path_in_repo=shard_name,
                    path_in_repo=shard_name
                )
            )
            missing_shards += 1

    print(f"📦 Total missing shards to transfer: {missing_shards}")

    # 2. Add Dual-License README and LICENSE_ENTERPRISE
    if os.path.exists(README_PATH):
        with open(README_PATH, "rb") as f:
            operations.append(CommitOperationAdd(path_in_repo="README.md", path_or_fileobj=f.read()))
        print("📝 Added updated Dual-License README.md to commit operations")

    if os.path.exists(LICENSE_PATH):
        with open(LICENSE_PATH, "rb") as f:
            operations.append(CommitOperationAdd(path_in_repo="LICENSE_ENTERPRISE.md", path_or_fileobj=f.read()))
        print("🛡️ Added LICENSE_ENTERPRISE.md to commit operations")

    if not operations:
        print("🎉 Everything is already synchronized in Kronumos-Aion!")
        return

    print(f"🚀 Committing {len(operations)} operations in a SINGLE atomic commit...")
    try:
        commit_info = api.create_commit(
            repo_id=DEST_REPO,
            repo_type="model",
            operations=operations,
            commit_message=f"Sync Dual Commercial/Academic License and transfer {missing_shards} safetensors shards"
        )
        print(f"🎉 SUKSES! All operations committed: {commit_info.commit_id}")
    except Exception as e:
        print(f"\n❌ Commit failed (if rate limit 429, wait for hourly window to reset): {e}")

if __name__ == "__main__":
    main()
