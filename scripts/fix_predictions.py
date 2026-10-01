#!/usr/bin/env python3
"""
fix_predictions.py — Post-process Kronumos predictions.jsonl (zero-dependency)
================================================================================
Fixes two systematic bugs in the runner's fallback diff generation:

1. MISSING CONTEXT LINES: 304/393 patches are "fallback diffs" with only -/+ lines.
   git apply needs context lines to locate the hunk.

2. PATH PREFIX: ~8 patches have bare paths missing repo package prefix.

Strategy:
  - Download SWE-bench_Verified instance info (repo + base_commit) from HuggingFace
  - For each fallback patch, fetch real source file from GitHub
  - Apply -/+ changes to reconstruct new file, recompute unified diff with context
  - Zero external dependencies (stdlib only)

Usage:
  export GITHUB_TOKEN=ghp_...
  python3 scripts/fix_predictions.py --input predictions.jsonl --output predictions_fixed.jsonl
"""

import os
import sys
import json
import time
import difflib
import argparse
import re
import urllib.request
import urllib.error
from typing import Optional, Dict, Tuple, List


# ── SWE-bench Dataset Download (via HuggingFace API, no datasets lib) ────────

def download_swebench_instances(cache_path: str = "/tmp/swebench_verified.jsonl") -> Dict[str, Dict]:
    """Download SWE-bench_Verified test split from HuggingFace Hub API."""
    if os.path.exists(cache_path):
        print(f"Using cached SWE-bench data: {cache_path}", flush=True)
        instances = {}
        with open(cache_path, "r") as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    instances[item["instance_id"]] = item
        if len(instances) > 400:
            return instances

    print("Downloading SWE-bench_Verified from HuggingFace...", flush=True)
    base_url = "https://datasets-server.huggingface.co/rows"
    headers = {"User-Agent": "Mozilla/5.0 (Kronumos-Patch-Fixer)"}
    instances = {}
    batch_size = 100
    offset = 0

    with open(cache_path, "w") as f:
        while True:
            url = f"{base_url}?dataset=princeton-nlp%2FSWE-bench_Verified&config=default&split=test&offset={offset}&length={batch_size}"
            req = urllib.request.Request(url, headers=headers)
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
            except Exception as e:
                print(f"  Fetch error at offset {offset}: {e}", flush=True)
                break

            rows = data.get("rows", [])
            if not rows:
                break

            for row in rows:
                item = row.get("row", {})
                iid = item.get("instance_id", "")
                if iid and iid not in instances:
                    instances[iid] = {
                        "instance_id": iid,
                        "repo": item.get("repo", ""),
                        "base_commit": item.get("base_commit", ""),
                        "version": item.get("version", ""),
                    }
                    f.write(json.dumps(instances[iid]) + "\n")

            print(f"  Downloaded {len(instances)} instances (offset={offset})...", flush=True)
            offset += len(rows)

            if len(rows) < batch_size:
                break

    print(f"Total SWE-bench instances loaded: {len(instances)}", flush=True)
    return instances


# ── GitHub File Fetching ─────────────────────────────────────────────

SWE_CACHE_DIR = "/tmp/swe_file_cache_fix"
os.makedirs(SWE_CACHE_DIR, exist_ok=True)

_rate_limit_wait_until = 0.0
_request_count = 0


def fetch_github_file(repo: str, commit: str, path: str, token: str = "") -> Optional[str]:
    """Fetch raw file from GitHub with caching and rate-limit awareness."""
    global _rate_limit_wait_until, _request_count

    clean_path = path.lstrip("/").replace("//", "/")
    cache_key = f"{repo.replace('/', '_')}_{commit[:10]}_{clean_path.replace('/', '_')}"
    cache_file = os.path.join(SWE_CACHE_DIR, cache_key)

    # Check cache first
    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
                if content:
                    return content
        except Exception:
            pass

    # Respect rate limit backoff
    now = time.time()
    if now < _rate_limit_wait_until:
        wait = _rate_limit_wait_until - now
        if wait > 0:
            print(f"    Rate limit: waiting {wait:.0f}s...", flush=True)
            time.sleep(wait)

    url = f"https://raw.githubusercontent.com/{repo}/{commit}/{clean_path}"
    headers = {"User-Agent": "Mozilla/5.0 (Kronumos-Patch-Fixer)"}
    if token:
        headers["Authorization"] = f"token {token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            _request_count += 1
            remaining = resp.headers.get("X-RateLimit-Remaining", "")
            if remaining:
                try:
                    rem = int(remaining)
                    if rem < 10:
                        reset_ts = int(resp.headers.get("X-RateLimit-Reset", "0"))
                        if reset_ts > 0:
                            _rate_limit_wait_until = reset_ts + 1
                    if _request_count % 50 == 0:
                        print(f"    GitHub API: {_request_count} requests, {rem} remaining", flush=True)
                except ValueError:
                    pass

            content = resp.read().decode("utf-8", errors="replace")
            try:
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception:
                pass
            return content
    except urllib.error.HTTPError as e:
        if e.code == 403:
            try:
                reset_ts = int(e.headers.get("X-RateLimit-Reset", "0"))
            except (ValueError, TypeError):
                reset_ts = 0
            if reset_ts > 0:
                _rate_limit_wait_until = reset_ts + 1
                wait = max(0, reset_ts - time.time())
                print(f"    Rate limited! Waiting {wait:.0f}s...", flush=True)
                time.sleep(wait + 1)
                return fetch_github_file(repo, commit, path, token)
        return None
    except Exception:
        return None


# ── Patch Parsing ────────────────────────────────────────────────────

def parse_patch(patch_text: str) -> Dict:
    """Parse a unified diff patch into structured components."""
    result = {
        "file_path": "",
        "orig_lines": [],
        "new_lines": [],
        "has_context": False,
        "hunk_start": 1,
        "raw_diff_lines": [],  # lines after @@ header
    }

    lines = patch_text.split("\n")
    in_hunk = False

    for line in lines:
        if line.startswith("--- a/"):
            result["file_path"] = line[6:]
        elif line.startswith("@@"):
            in_hunk = True
            m = re.match(r"@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@", line)
            if m:
                result["hunk_start"] = int(m.group(1))
        elif in_hunk:
            result["raw_diff_lines"].append(line)
            if line.startswith("-"):
                result["orig_lines"].append(line[1:])
            elif line.startswith("+"):
                result["new_lines"].append(line[1:])
            elif line.startswith(" "):
                result["has_context"] = True
                result["orig_lines"].append(line[1:])
                result["new_lines"].append(line[1:])

    return result


def fix_path_prefix(file_path: str, repo: str) -> str:
    """Fix missing package directory prefix in file paths."""
    if not file_path or not repo:
        return file_path

    parts = repo.split("/")
    if len(parts) != 2:
        return file_path

    pkg_dir = parts[1]

    if file_path.startswith(f"{pkg_dir}/"):
        return file_path

    skip_prefixes = ["tests/", "test/", "setup.", "docs/", "doc/", "LICENSE", "README",
                     "MANIFEST", "tox.ini", "conftest", ".github/", "Makefile",
                     "manage.py", "pyproject.toml"]
    for sp in skip_prefixes:
        if file_path.startswith(sp) or file_path == sp.rstrip("/"):
            return file_path

    return f"{pkg_dir}/{file_path}"


def find_best_match(file_content: str, orig_lines: List[str]) -> Tuple[int, int, float]:
    """Find the best matching region in the file for the original lines using fast anchor search.
    
    Returns (best_start, best_window, best_ratio).
    """
    file_lines = file_content.splitlines()
    orig_stripped = [l.strip() for l in orig_lines if l.strip()]
    if not orig_stripped:
        return -1, 0, 0.0

    file_stripped = [l.strip() for l in file_lines]
    target_str = "\n".join(orig_stripped)
    target_len = len(orig_stripped)

    # 1. Fast exact contiguous block match
    for i in range(len(file_stripped) - target_len + 1):
        if file_stripped[i:i + target_len] == orig_stripped:
            return i, target_len, 1.0

    # 2. Anchor search: find positions matching the most distinctive line
    # Sort lines by length to find the most unique non-trivial anchor
    anchor_candidates = sorted(
        [(idx, l) for idx, l in enumerate(orig_stripped) if len(l) > 6 and not l.startswith(("#", "//", '"""', "'''"))],
        key=lambda x: len(x[1]),
        reverse=True
    )

    cand_starts = set()
    for anchor_idx, anchor_line in anchor_candidates[:3]:
        for i, fl in enumerate(file_stripped):
            if anchor_line == fl or (len(anchor_line) > 15 and anchor_line in fl):
                start = i - anchor_idx
                if 0 <= start <= len(file_stripped) - target_len:
                    cand_starts.add(start)
        if len(cand_starts) > 0 and len(cand_starts) <= 10:
            break

    # If no anchors matched, try first and last non-empty lines
    if not cand_starts:
        for anchor_idx, anchor_line in [(0, orig_stripped[0]), (target_len - 1, orig_stripped[-1])]:
            for i, fl in enumerate(file_stripped):
                if anchor_line == fl:
                    start = i - anchor_idx
                    if 0 <= start <= len(file_stripped) - target_len:
                        cand_starts.add(start)

    # If still no candidates, do a sampled step search instead of every single line
    if not cand_starts:
        step = max(1, target_len // 2)
        cand_starts = set(range(0, len(file_stripped) - target_len + 1, step))

    # Evaluate candidates with SequenceMatcher
    best_ratio = 0.0
    best_start = -1
    best_window = target_len

    min_w = max(1, target_len - 2)
    max_w = min(len(file_lines), target_len + 2)

    for start in cand_starts:
        for w in range(min_w, max_w + 1):
            if start + w <= len(file_stripped):
                cand = file_stripped[start:start + w]
                cand_str = "\n".join(cand)
                ratio = difflib.SequenceMatcher(None, target_str, cand_str).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_start = start
                    best_window = w
                    if ratio >= 0.95:
                        return best_start, best_window, best_ratio

    return best_start, best_window, best_ratio


def reconstruct_and_diff(file_content: str, orig_lines: List[str], new_lines: List[str],
                          file_path: str) -> Optional[str]:
    """Apply changes and produce a proper unified diff with context lines."""
    file_lines_raw = file_content.splitlines(keepends=True)

    # First try exact match of original text
    orig_text = "\n".join(orig_lines)
    if orig_text.strip() and orig_text in file_content:
        new_text = "\n".join(new_lines)
        new_content = file_content.replace(orig_text, new_text, 1)
        diff = list(difflib.unified_diff(
            file_lines_raw,
            new_content.splitlines(keepends=True),
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}",
        ))
        if diff:
            return f"diff --git a/{file_path} b/{file_path}\n" + "".join(diff)

    # Sliding window match
    best_start, best_window, best_ratio = find_best_match(file_content, orig_lines)

    if best_ratio < 0.40 or best_start < 0:
        return None

    # Detect anchor indentation from target file location
    anchor_line = file_lines_raw[best_start] if best_start < len(file_lines_raw) else ""
    anchor_indent = anchor_line[:len(anchor_line) - len(anchor_line.lstrip())]

    orig_code_str = "\n".join(orig_lines)
    new_code_str = "\n".join(new_lines)

    # ⚡ Zero-Token Native Rust Sub-Cortex Indentation Healing:
    # Eliminates Python IndentationError by rebasing to target anchor indent in microseconds
    try:
        from scripts.tokenectomy_subcortex_rust import RustSubCortex
        healed_new_str = RustSubCortex.heal_indentation(orig_code_str, new_code_str, anchor_indent)
    except Exception:
        healed_new_str = new_code_str

    healed_replacement = [l + "\n" for l in healed_new_str.splitlines()]
    reconstructed = file_lines_raw[:best_start] + healed_replacement + file_lines_raw[best_start + best_window:]
    reconstructed_str = "".join(reconstructed)

    # Verify that the reconstructed file compiles cleanly as Python AST
    if file_path.endswith(".py"):
        try:
            import ast
            ast.parse(reconstructed_str)
        except (SyntaxError, IndentationError):
            # If healed version had syntax issues, test original new_lines fallback
            replacement_raw = [l + "\n" for l in new_lines]
            reconstructed_raw = file_lines_raw[:best_start] + replacement_raw + file_lines_raw[best_start + best_window:]
            try:
                import ast
                ast.parse("".join(reconstructed_raw))
                reconstructed = reconstructed_raw
            except Exception:
                pass

    diff = list(difflib.unified_diff(
        file_lines_raw,
        reconstructed,
        fromfile=f"a/{file_path}",
        tofile=f"b/{file_path}",
    ))
    if diff:
        return f"diff --git a/{file_path} b/{file_path}\n" + "".join(diff)
    return None


# ── Main Pipeline ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fix Kronumos prediction patches (zero-dependency)")
    parser.add_argument("--input", default="predictions.jsonl", help="Input predictions.jsonl")
    parser.add_argument("--output", default="predictions_fixed.jsonl", help="Output fixed predictions")
    parser.add_argument("--dry-run", action="store_true", help="Analyze without writing output")
    args = parser.parse_args()

    token = os.getenv("GITHUB_TOKEN", "").strip() or os.getenv("GH_TOKEN", "").strip()
    if not token:
        print("WARNING: No GITHUB_TOKEN set. Rate limited to 60 req/hr.")
        print("Set GITHUB_TOKEN=ghp_... for 5000 req/hr.\n")

    # Load SWE-bench instance info
    instance_info = download_swebench_instances()

    # Load predictions
    predictions = []
    with open(args.input) as f:
        for line in f:
            if line.strip():
                predictions.append(json.loads(line))
    print(f"Loaded {len(predictions)} predictions.\n", flush=True)

    # Stats
    stats = {
        "total": 0, "empty": 0, "already_good": 0,
        "fixed": 0, "path_fixed": 0,
        "fetch_failed": 0, "match_failed": 0, "no_info": 0,
    }
    fixed_predictions = []

    for idx, pred in enumerate(predictions):
        stats["total"] += 1
        iid = pred.get("instance_id", "")
        patch = pred.get("model_patch", "")

        if not patch.strip():
            stats["empty"] += 1
            fixed_predictions.append(pred)
            continue

        parsed = parse_patch(patch)

        if parsed["has_context"]:
            stats["already_good"] += 1
            fixed_predictions.append(pred)
            continue

        # Get instance info
        info = instance_info.get(iid)
        if not info or not info.get("repo") or not info.get("base_commit"):
            stats["no_info"] += 1
            fixed_predictions.append(pred)
            continue

        repo = info["repo"]
        commit = info["base_commit"]
        file_path = parsed["file_path"]

        # Fix path prefix
        fixed_path = fix_path_prefix(file_path, repo)
        if fixed_path != file_path:
            stats["path_fixed"] += 1

        # Fetch source file
        file_content = fetch_github_file(repo, commit, fixed_path, token=token)
        if file_content is None and fixed_path != file_path:
            file_content = fetch_github_file(repo, commit, file_path, token=token)
            if file_content is not None:
                fixed_path = file_path

        if file_content is None:
            stats["fetch_failed"] += 1
            # At minimum fix path in original patch
            if fixed_path != file_path:
                patch = patch.replace(file_path, fixed_path)
                pred = {**pred, "model_patch": patch}
            fixed_predictions.append(pred)
            prog = f"[{idx+1}/{len(predictions)}]"
            print(f"  {prog} {iid}: FETCH FAILED ({fixed_path})", flush=True)
            continue

        # Reconstruct and recompute diff
        new_diff = reconstruct_and_diff(
            file_content, parsed["orig_lines"], parsed["new_lines"], fixed_path
        )
        if new_diff is None:
            stats["match_failed"] += 1
            if fixed_path != file_path:
                patch = patch.replace(file_path, fixed_path)
                pred = {**pred, "model_patch": patch}
            fixed_predictions.append(pred)
            prog = f"[{idx+1}/{len(predictions)}]"
            print(f"  {prog} {iid}: MATCH FAILED", flush=True)
            continue

        stats["fixed"] += 1
        pred = {**pred, "model_patch": new_diff}
        fixed_predictions.append(pred)

        prog = f"[{idx+1}/{len(predictions)}]"
        print(f"  {prog} {iid}: FIXED ({fixed_path})", flush=True)

    # Summary
    print("\n" + "=" * 60)
    print("FIX PREDICTIONS SUMMARY")
    print("=" * 60)
    for k, v in stats.items():
        print(f"  {k:20s}: {v}")
    print(f"  {'github_requests':20s}: {_request_count}")
    print("=" * 60)

    if not args.dry_run:
        with open(args.output, "w") as f:
            for pred in fixed_predictions:
                f.write(json.dumps(pred) + "\n")
        print(f"\nWritten to: {args.output}")
    else:
        print("\nDry run — no output written.")


if __name__ == "__main__":
    main()
