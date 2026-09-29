#!/usr/bin/env python3
"""
⚡ Tokenectomy Sub-Cortex: Predictions Diff Re-Anchoring & Healer
================================================================
Re-anchors unanchored patches (such as those malformed with `@@ -1,x`)
by fetching the ground-truth base commit file and calculating exact
unified diff hunks with correct line offsets and 3-line context.

Usage:
  python3 scripts/heal_predictions.py --input predictions.jsonl --output predictions_healed.jsonl
"""

import os
import re
import json
import difflib
import argparse
import urllib.request
import urllib.error
import subprocess
from typing import Dict, Any, List, Optional, Tuple

SWE_CACHE_DIR = "/tmp/swe_file_cache"
os.makedirs(SWE_CACHE_DIR, exist_ok=True)


def fetch_github_file(repo: str, base_commit: str, file_path: str, token: str = "") -> Optional[str]:
    """
    Fetch raw file content with 4-tier resilience:
    1. Persistent local disk cache (/tmp/swe_file_cache).
    2. Local git repository checkout if available.
    3. raw.githubusercontent.com.
    4. Authenticated GitHub REST API fallback.
    """
    clean_path = file_path.lstrip("/").replace("//", "/")
    cache_key = f"{repo.replace('/', '_')}_{base_commit[:10]}_{clean_path.replace('/', '_')}"
    cache_file = os.path.join(SWE_CACHE_DIR, cache_key)

    if os.path.exists(cache_file):
        try:
            with open(cache_file, "r", encoding="utf-8", errors="replace") as f:
                return f.read()
        except Exception:
            pass

    repo_short = repo.split("/")[-1] if "/" in repo else repo
    repo_search_dirs = [
        os.path.join(os.getenv("SWE_BENCH_REPOS_DIR", "/tmp/repos"), repo.replace("/", "__")),
        os.path.join(os.getenv("SWE_BENCH_REPOS_DIR", "/tmp/repos"), repo_short),
        os.path.join("/tmp/repos", repo_short),
        os.path.join("./repos", repo_short),
    ]
    for rdir in repo_search_dirs:
        if os.path.isdir(os.path.join(rdir, ".git")):
            try:
                proc = subprocess.run(
                    ["git", "show", f"{base_commit}:{clean_path}"],
                    cwd=rdir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=5
                )
                if proc.returncode == 0 and proc.stdout:
                    try:
                        with open(cache_file, "w", encoding="utf-8") as f:
                            f.write(proc.stdout)
                    except Exception:
                        pass
                    return proc.stdout
            except Exception:
                pass

    auth_token = token or os.getenv("GITHUB_TOKEN", "").strip() or os.getenv("GH_TOKEN", "").strip()

    url = f"https://raw.githubusercontent.com/{repo}/{base_commit}/{clean_path}"
    headers = {"User-Agent": "Mozilla/5.0 (Tokenectomy-Patch-Healer)"}
    if auth_token:
        headers["Authorization"] = f"token {auth_token}"

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            try:
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception:
                pass
            return content
    except Exception:
        pass

    api_url = f"https://api.github.com/repos/{repo}/contents/{clean_path}?ref={base_commit}"
    api_headers = {
        "User-Agent": "Tokenectomy-Patch-Healer",
        "Accept": "application/vnd.github.v3.raw"
    }
    if auth_token:
        api_headers["Authorization"] = f"Bearer {auth_token}"
    req_api = urllib.request.Request(api_url, headers=api_headers)
    try:
        with urllib.request.urlopen(req_api, timeout=12) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            try:
                with open(cache_file, "w", encoding="utf-8") as f:
                    f.write(content)
            except Exception:
                pass
            return content
    except Exception:
        return None


def parse_diff_hunks(diff_text: str) -> List[Dict[str, Any]]:
    """
    Extracts target file path, original code lines (-), and new code lines (+)
    from an existing diff string.
    """
    hunks = []
    # Identify file path
    f_match = re.search(r"--- a/([^\s\n]+)", diff_text)
    if not f_match:
        f_match = re.search(r"diff --git a/([^\s\n]+) b/", diff_text)
    if not f_match:
        return hunks

    file_path = f_match.group(1).strip()
    
    # Split by hunk headers: @@ -... +... @@
    hunk_parts = re.split(r"(@@\s+-[0-9]+(?:,[0-9]+)?\s+\+[0-9]+(?:,[0-9]+)?\s+@@)", diff_text)
    if len(hunk_parts) < 3:
        # Fallback: scan lines directly
        lines = diff_text.splitlines()
        orig_lines = []
        new_lines = []
        in_hunk = False
        for line in lines:
            if line.startswith("@@"):
                in_hunk = True
                continue
            if not in_hunk:
                continue
            if line.startswith("-") and not line.startswith("---"):
                orig_lines.append(line[1:])
            elif line.startswith("+") and not line.startswith("+++"):
                new_lines.append(line[1:])
            elif line.startswith(" "):
                orig_lines.append(line[1:])
                new_lines.append(line[1:])
        if orig_lines or new_lines:
            hunks.append({
                "file_path": file_path,
                "orig_lines": orig_lines,
                "new_lines": new_lines
            })
        return hunks

    # Iterate pairs of header + body
    for i in range(1, len(hunk_parts), 2):
        header = hunk_parts[i]
        body = hunk_parts[i + 1] if i + 1 < len(hunk_parts) else ""
        orig_lines = []
        new_lines = []
        for line in body.splitlines():
            if line.startswith("-") and not line.startswith("---"):
                orig_lines.append(line[1:])
            elif line.startswith("+") and not line.startswith("+++"):
                new_lines.append(line[1:])
            elif line.startswith(" "):
                orig_lines.append(line[1:])
                new_lines.append(line[1:])
        hunks.append({
            "header": header,
            "file_path": file_path,
            "orig_lines": orig_lines,
            "new_lines": new_lines
        })
    return hunks


def reanchor_patch(
    repo: str,
    base_commit: str,
    diff_text: str,
    token: str = ""
) -> Tuple[Optional[str], str]:
    """
    Attempts to locate the removed lines in the real file and regenerate
    a clean unified diff with correct line numbers and context lines.
    """
    hunks = parse_diff_hunks(diff_text)
    if not hunks:
        return None, "No hunks or file path detected in diff"

    file_path = hunks[0]["file_path"]
    raw_content = fetch_github_file(repo, base_commit, file_path, token=token)
    if not raw_content:
        return None, f"Could not fetch source file {file_path} from GitHub or cache"

    file_lines = raw_content.splitlines(keepends=True)
    orig_code_str = "\n".join(hunks[0]["orig_lines"])
    new_code_str = "\n".join(hunks[0]["new_lines"])

    # 1. Exact match search
    if orig_code_str in raw_content:
        new_content = raw_content.replace(orig_code_str, new_code_str, 1)
        healed_diff = list(difflib.unified_diff(
            file_lines,
            new_content.splitlines(keepends=True),
            fromfile=f"a/{file_path}",
            tofile=f"b/{file_path}"
        ))
        if healed_diff:
            return "".join(healed_diff), "Exact match re-anchored"

    # 2. Trimmed match search
    stripped_target = [l.strip() for l in hunks[0]["orig_lines"] if l.strip()]
    if stripped_target:
        window_size = len(stripped_target)
        target_str = "\n".join(stripped_target)
        best_ratio = 0.0
        best_start = -1
        for i in range(len(file_lines)):
            cand_slice = [file_lines[i + k].strip() for k in range(window_size) if i + k < len(file_lines)]
            cand_str = "\n".join(cand_slice)
            ratio = difflib.SequenceMatcher(None, target_str, cand_str).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_start = i

        if best_ratio >= 0.50 and best_start >= 0:
            anchor_line = file_lines[best_start]
            indent = anchor_line[:len(anchor_line) - len(anchor_line.lstrip())]
            formatted_plus = [indent + p.lstrip() + "\n" if p.strip() else "\n" for p in hunks[0]["new_lines"]]
            new_lines = file_lines[:best_start] + formatted_plus + file_lines[best_start + window_size:]
            healed_diff = list(difflib.unified_diff(
                file_lines,
                new_lines,
                fromfile=f"a/{file_path}",
                tofile=f"b/{file_path}"
            ))
            if healed_diff:
                return "".join(healed_diff), f"Fuzzy match re-anchored ({round(best_ratio*100)}% match at line {best_start+1})"

    return None, f"Original snippet not locatable in {file_path}"


def main():
    parser = argparse.ArgumentParser(description="Heal unanchored predictions in predictions.jsonl")
    parser.add_argument("--input", type=str, default="predictions.jsonl", help="Input predictions file")
    parser.add_argument("--output", type=str, default="predictions_healed.jsonl", help="Output healed file")
    parser.add_argument("--metadata", type=str, default="dataset/swebench_verified_metadata.json", help="Metadata file")
    parser.add_argument("--token", type=str, default="", help="GitHub token for raw API fetches")
    parser.add_argument("--heal_all", action="store_true", help="Attempt to re-anchor all non-empty patches, not just @@ -1")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"❌ Input file {args.input} does not exist.")
        return

    metadata = {}
    if os.path.exists(args.metadata):
        with open(args.metadata, "r", encoding="utf-8") as f:
            metadata = json.load(f)
        print(f"📦 Loaded metadata for {len(metadata)} instances.")
    else:
        print(f"⚠️ Metadata file {args.metadata} not found. Will infer repo from instance_id.")

    records = []
    with open(args.input, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    pass

    print(f"🔍 Inspecting {len(records)} predictions from {args.input}...")

    total_corrupted = 0
    total_healed = 0
    total_retained = 0
    unhealed_instances = []

    healed_records = []

    for item in records:
        iid = item.get("instance_id", "")
        patch = item.get("model_patch", "")
        needs_healing = False

        if patch:
            if "@@ -1," in patch:
                needs_healing = True
                total_corrupted += 1
            elif args.heal_all:
                needs_healing = True

        if needs_healing:
            meta = metadata.get(iid, {})
            repo = meta.get("repo", "")
            base_commit = meta.get("base_commit", "")
            if not repo and "-" in iid:
                repo = iid.rsplit("-", 1)[0].replace("__", "/")

            if repo and base_commit:
                healed_diff, msg = reanchor_patch(repo, base_commit, patch, token=args.token)
                if healed_diff:
                    item["model_patch"] = healed_diff
                    total_healed += 1
                    print(f"  ✅ [{iid}] {msg}")
                else:
                    unhealed_instances.append((iid, msg))
                    print(f"  ⚠️ [{iid}] Could not heal: {msg}")
            else:
                unhealed_instances.append((iid, "Missing base_commit"))
                print(f"  ⚠️ [{iid}] Missing repo or base_commit.")
        else:
            if patch:
                total_retained += 1

        healed_records.append(item)

    with open(args.output, "w", encoding="utf-8") as f:
        for r in healed_records:
            f.write(json.dumps(r) + "\n")

    print("\n" + "=" * 60)
    print("🎯 Patch Healing Summary:")
    print(f"  Total records:            {len(records)}")
    print(f"  Broken patches detected:  {total_corrupted}")
    print(f"  Successfully healed:      {total_healed}")
    print(f"  Clean patches retained:   {total_retained}")
    print(f"  Failed to heal:           {len(unhealed_instances)}")
    print(f"  Output saved to:          {args.output}")
    print("=" * 60)


if __name__ == "__main__":
    main()
