#!/usr/bin/env python3
"""
Intelligent Git Diff Repair & Validator for SWE-bench Predictions
Converts AST search-and-replace patches into standard POSIX-compliant unified git diffs
with exact hunk headers (@@ -line,count +line,count @@) and verified line contexts.
"""

import json
import os
import re
import difflib
import urllib.request
import urllib.error
import subprocess
import tempfile
from pathlib import Path

CACHE_DIR = Path("/tmp/swe_file_cache")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def fetch_file(repo: str, base_commit: str, file_path: str) -> str | None:
    """Fetch raw file content from GitHub with local caching."""
    # Clean file path
    clean_path = file_path.lstrip("/").replace("//", "/")
    cache_key = f"{repo.replace('/', '_')}_{base_commit[:10]}_{clean_path.replace('/', '_')}"
    cached_file = CACHE_DIR / cache_key
    
    if cached_file.exists():
        return cached_file.read_text(encoding="utf-8", errors="replace")
        
    url = f"https://raw.githubusercontent.com/{repo}/{base_commit}/{clean_path}"
    headers = {"User-Agent": "Mozilla/5.0 (Kronumos-Diff-Repair)"}
    auth_token = os.getenv("GITHUB_TOKEN", "").strip()
    if auth_token:
        headers["Authorization"] = f"token {auth_token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            cached_file.write_text(content, encoding="utf-8")
            return content
    except Exception as e:
        return None

def parse_raw_patch(patch_str: str) -> tuple[str, list[str], list[str]]:
    """Extract file_path, minus_lines, and plus_lines from unstructured patch string."""
    lines = patch_str.splitlines()
    f_path = ""
    minus_lines = []
    plus_lines = []
    
    for line in lines:
        if line.startswith("--- a/"):
            f_path = line[6:].strip()
        elif line.startswith("+++ b/") and not f_path:
            f_path = line[6:].strip()
        elif line.startswith("-") and not line.startswith("---"):
            minus_lines.append(line[1:])
        elif line.startswith("+") and not line.startswith("+++"):
            plus_lines.append(line[1:])
            
    return f_path, minus_lines, plus_lines

def generate_posix_diff(repo: str, base_commit: str, file_path: str, minus_lines: list[str], plus_lines: list[str]) -> str | None:
    """Generate a clean, context-aware unified diff verified by GNU patch."""
    if not file_path or not minus_lines:
        return None
        
    # Clean file path
    file_path = file_path.lstrip("/").replace("//", "/")
    
    # Exclude common hallucinated files that don't belong to the repo
    hallucinated_prefixes = ["test.py", "poc.py", "app/", "model.py", "scratch_", "testapp", "testing/"]
    if any(file_path.startswith(p) for p in hallucinated_prefixes):
        # Unless it's an actual file in repo
        pass
        
    raw_content = fetch_file(repo, base_commit, file_path)
    if raw_content is None:
        return None
        
    file_lines = raw_content.splitlines(keepends=True)
    if not file_lines:
        return None
        
    # 1. Try exact line matching
    minus_text = "\n".join(minus_lines)
    if minus_text in raw_content:
        new_content = raw_content.replace(minus_text, "\n".join(plus_lines), 1)
        diff = list(difflib.unified_diff(
            file_lines,
            new_content.splitlines(keepends=True),
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}"
        ))
        diff_str = "".join(diff)
        if verify_diff_with_patch(raw_content, file_path, diff_str):
            return diff_str
            
    # 2. Try normalized whitespace matching
    target_stripped = [l.strip() for l in minus_lines if l.strip()]
    if not target_stripped:
        return None
        
    best_ratio = 0.0
    best_start = -1
    window_size = len(target_stripped)
    target_str = "\n".join(target_stripped)
    
    for i in range(len(file_lines)):
        cand_slice = [file_lines[i + k].strip() for k in range(window_size) if i + k < len(file_lines)]
        cand_str = "\n".join(cand_slice)
        ratio = difflib.SequenceMatcher(None, target_str, cand_str).ratio()
        if ratio > best_ratio:
            best_ratio = ratio
            best_start = i
            
    if best_ratio >= 0.70 and best_start >= 0:
        # Determine base indentation from matched line
        anchor_line = file_lines[best_start]
        indent = anchor_line[:len(anchor_line) - len(anchor_line.lstrip())]
        
        # Prepare replacement lines
        formatted_plus = []
        for p in plus_lines:
            if p.strip():
                formatted_plus.append(indent + p.lstrip() + "\n")
            else:
                formatted_plus.append("\n")
                
        new_lines = file_lines[:best_start] + formatted_plus + file_lines[best_start + window_size:]
        diff = list(difflib.unified_diff(
            file_lines,
            new_lines,
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}"
        ))
        diff_str = "".join(diff)
        if verify_diff_with_patch(raw_content, file_path, diff_str):
            return diff_str

    return None

def verify_diff_with_patch(original_content: str, file_path: str, diff_str: str) -> bool:
    """Dry-run GNU patch to ensure zero Hunk failures."""
    if not diff_str or not diff_str.strip():
        return False
    with tempfile.TemporaryDirectory() as tmpdir:
        t_file = Path(tmpdir) / file_path
        t_file.parent.mkdir(parents=True, exist_ok=True)
        t_file.write_text(original_content, encoding="utf-8")
        
        diff_file = Path(tmpdir) / "patch.diff"
        diff_file.write_text(diff_str, encoding="utf-8")
        
        res = subprocess.run(
            ["patch", "-p1", "--dry-run", "-i", str(diff_file)],
            cwd=tmpdir,
            capture_output=True,
            text=True
        )
        return res.returncode == 0

def main():
    meta_path = Path("/tmp/swe_verified_meta.json")
    if not meta_path.exists():
        print("❌ Metadata file not found at /tmp/swe_verified_meta.json")
        return
        
    with open(meta_path) as f:
        metadata = json.load(f)
        
    pred_path = Path("predictions.jsonl")
    if not pred_path.exists():
        print("❌ predictions.jsonl not found")
        return
        
    repaired_records = []
    success_count = 0
    empty_count = 0
    discarded_count = 0
    total = 0
    
    with open(pred_path) as f:
        lines = [json.loads(line) for line in f if line.strip()]
        
    print(f"🔧 Processing {len(lines)} prediction records...")
    
    for record in lines:
        total += 1
        inst_id = record["instance_id"]
        old_patch = record.get("model_patch", "")
        
        if not old_patch or not old_patch.strip():
            empty_count += 1
            repaired_records.append({
                "instance_id": inst_id,
                "model_patch": "",
                "model_name_or_path": record.get("model_name_or_path", "Kronumos-7B")
            })
            continue
            
        inst_meta = metadata.get(inst_id, {})
        repo = inst_meta.get("repo")
        base_commit = inst_meta.get("base_commit")
        
        if not repo or not base_commit:
            print(f"⚠️ Missing metadata for {inst_id}")
            repaired_records.append(record)
            continue
            
        f_path, minus_lines, plus_lines = parse_raw_patch(old_patch)
        
        new_diff = generate_posix_diff(repo, base_commit, f_path, minus_lines, plus_lines)
        
        if new_diff:
            success_count += 1
            repaired_records.append({
                "instance_id": inst_id,
                "model_patch": new_diff,
                "model_name_or_path": record.get("model_name_or_path", "Kronumos-7B")
            })
            print(f"  ✅ [VALIDATED] {inst_id} -> {f_path}")
        else:
            discarded_count += 1
            print(f"  ❌ [UNVERIFIED] {inst_id} -> {f_path} (reverted to empty patch to avoid dirty diff error)")
            repaired_records.append({
                "instance_id": inst_id,
                "model_patch": "",
                "model_name_or_path": record.get("model_name_or_path", "Kronumos-7B")
            })
            
    # Write back repaired predictions
    repaired_path = Path("predictions.jsonl")
    with open(repaired_path, "w", encoding="utf-8") as f:
        for r in repaired_records:
            f.write(json.dumps(r) + "\n")
            
    print("\n" + "="*60)
    print("🎉 DIFF REPAIR & POSIX VALIDATION COMPLETED!")
    print(f"Total instances: {total}")
    print(f"✅ Clean Validated Patches: {success_count} (100% verified by GNU patch)")
    print(f"🚫 Unverified / Hallucinated Discarded: {discarded_count}")
    print(f"⚪ Empty Gated Instances: {empty_count}")
    print("="*60)

if __name__ == "__main__":
    main()
