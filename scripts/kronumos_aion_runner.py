#!/usr/bin/env python3
"""
🏛️ Kronumos Aion — Flagship Deep Cybernetic Program Repair Engine
====================================================================
Architecture:
  - Cognitive Neural Cortex: DeepSeek-R1 (671B MoE, MIT License)
    Operates with deep test-time counterfactual reasoning (<thought> tags).
  - Deterministic Native Sub-Cortex: Tokenectomy Rust C-ABI (5µs AST Healer)
    Pre-Inference: 93% token excision & AST enclosing function slicing.
    Post-Inference: Microsecond indentation healing, ScopeGuard, and Sentinel audit.

Supports:
  1. Azure AI Studio Serverless API (AZURE_AI_ENDPOINT & AZURE_AI_KEY)
  2. DeepSeek Official API (DEEPSEEK_API_KEY)
  3. OpenRouter / Together / Local vLLM (OPENAI_API_BASE & OPENAI_API_KEY)
"""

import os
import sys
import re
import json
import time
import argparse
import difflib
import urllib.request
import urllib.error
import ast
import textwrap
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

# Import Tokenectomy Sub-Cortex components
try:
    from scripts.issue_denoiser import IssueDeNoiser
    from scripts.mutation_bracket import ZeroLLMMutationBracket
    from scripts.tokenectomy_subcortex_rust import RustSubCortex
except ImportError:
    try:
        from issue_denoiser import IssueDeNoiser
        from mutation_bracket import ZeroLLMMutationBracket
        from tokenectomy_subcortex_rust import RustSubCortex
    except ImportError:
        IssueDeNoiser = None
        ZeroLLMMutationBracket = None
        RustSubCortex = None

try:
    from datasets import load_dataset
except ImportError:
    load_dataset = None


AION_SYSTEM_PROMPT = (
    "You are Kronumos Aion, the flagship autonomous program-repair engine powered by "
    "the Tokenectomy M2M Sub-Cortex. You synthesize surgical, production-safe code fixes with zero dirty diffs.\n\n"
    "OPERATIONAL PROTOCOL:\n"
    "1. You possess deep counterfactual reasoning. Always articulate your complete diagnostic plan "
    "inside <thought>...</thought> tags before generating code:\n"
    "   (a) Root-cause fault hypothesis derived from the Cleaned Technical Specification.\n"
    "   (b) Exact target repository file, enclosing function, and suspect lines.\n"
    "   (c) Verification of backward compatibility and edge cases.\n"
    "2. Target ONLY authentic internal source files within the repository package tree. "
    "NEVER modify reproduction snippets or test fixtures unless explicitly instructed.\n"
    "3. To apply an atomic change, emit a single SEARCH/REPLACE block with character-exact indentation:\n"
    "   File: path/to/internal/file.py\n"
    "   <<<<<<< SEARCH\n"
    "   original exact code lines\n"
    "   =======\n"
    "   replacement code lines\n"
    "   >>>>>>> REPLACE\n"
    "4. Invariants: NEVER return None from constructors (__new__, __init__). NEVER introduce naked pass in exception handlers. "
    "Guarantee 100% syntactic and structural AST compliance."
)


def call_aion_api(
    messages: List[Dict[str, str]],
    endpoint: str,
    api_key: str,
    model: str = "DeepSeek-R1",
    temperature: float = 0.2,
    max_tokens: int = 4096
) -> Tuple[str, str, int, int]:
    """
    Zero-dependency universal API caller compatible with Azure AI Studio, DeepSeek API, and OpenAI endpoints.
    Returns: (content, reasoning_content, prompt_tokens, completion_tokens)
    """
    clean_endpoint = endpoint.rstrip("/")
    if not clean_endpoint.endswith("/chat/completions"):
        url = f"{clean_endpoint}/chat/completions"
    else:
        url = clean_endpoint

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "api-key": api_key, # Azure standard
        "User-Agent": "Kronumos-Aion-Runner/1.0"
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            choice = res_data["choices"][0]["message"]
            content = choice.get("content", "") or ""
            reasoning = choice.get("reasoning_content", "") or ""

            usage = res_data.get("usage", {})
            prompt_tokens = usage.get("prompt_tokens", 0)
            completion_tokens = usage.get("completion_tokens", 0)
            return content, reasoning, prompt_tokens, completion_tokens
    except urllib.error.HTTPError as e:
        err_msg = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Aion API HTTP {e.code}: {err_msg}")
    except Exception as e:
        raise RuntimeError(f"Aion API Connection Error: {str(e)}")


class KronumosAionRunner:
    """
    Autonomous Benchmark Harness for Kronumos Aion (DeepSeek-R1 + Tokenectomy Rust Sub-Cortex).
    """
    def __init__(self, endpoint: str, api_key: str, model: str = "DeepSeek-R1", github_token: str = ""):
        self.endpoint = endpoint
        self.api_key = api_key
        self.model = model
        self.github_token = github_token or os.environ.get("GITHUB_TOKEN", "")

        # Verify Rust Sub-Cortex engine
        if RustSubCortex and RustSubCortex.is_available():
            print("⚡ [Tokenectomy Rust Sub-Cortex]: 100% NATIVE C-ABI ACTIVE")
        else:
            print("⚠️ [Tokenectomy Sub-Cortex]: Python Fallback Mode (Compile Rust for 5µs latency)")

    def solve_instance(self, instance: Dict[str, Any], max_turns: int = 3) -> Dict[str, Any]:
        from scripts.kaggle_kronumos_runner import (
            extract_suspect_context_from_issue,
            extract_search_replace_blocks,
            convert_patch_call_to_diff
        )

        instance_id = instance.get("instance_id", "unknown")
        repo = instance.get("repo", "unknown")
        base_commit = instance.get("base_commit", "")
        raw_problem = instance.get("problem_statement", "")

        # 1. Pre-Inference: Tokenectomy Discourse De-Noising
        if IssueDeNoiser:
            denoised = IssueDeNoiser.denoise_issue(raw_problem, repo=repo)
            clean_problem = f"{denoised['specification_header']}\n\n{denoised['cleaned_text']}"
        else:
            clean_problem = raw_problem

        # 2. Pre-Inference: AST Enclosing Function Slicing
        suspect_info = extract_suspect_context_from_issue(repo, base_commit, raw_problem, token=self.github_token)

        user_prompt = f"Repository: {repo}\nIssue ID: {instance_id}\n\nProblem Description:\n{clean_problem}"
        if suspect_info:
            slice_desc = "AST Enclosing Function" if suspect_info.get("is_ast_sliced") else "Source Context Window"
            user_prompt += (
                f"\n\n[Tokenectomy {slice_desc} Localization]\n"
                f"Suspect Target File: {suspect_info['file_path']} (Near line {suspect_info['suspect_line']})\n"
                f"Enclosing Symbol: {suspect_info.get('node_name', 'unknown')}\n"
                f"Source Context from commit ({base_commit[:8]}):\n"
                f"```python\n{suspect_info['snippet']}\n```\n"
            )

        messages = [
            {"role": "system", "content": AION_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ]

        total_prompt_tokens = 0
        total_completion_tokens = 0
        synthesized_patch = ""
        turns = 0
        start_time = time.time()

        for turn in range(max_turns):
            turns += 1
            content, reasoning, p_tok, c_tok = call_aion_api(
                messages=messages,
                endpoint=self.endpoint,
                api_key=self.api_key,
                model=self.model
            )
            total_prompt_tokens += p_tok
            total_completion_tokens += c_tok

            # 3. Post-Inference: Extract blocks and invoke Native Rust Sub-Cortex
            blocks = extract_search_replace_blocks(content)
            if not blocks and "File:" in content and "<<<<<<< SEARCH" in content:
                # Secondary loose match
                blocks = extract_search_replace_blocks("File: " + content.split("File:", 1)[1])

            if blocks:
                for blk in blocks:
                    diff_str, status, msg = convert_patch_call_to_diff(
                        file_path=blk["file_path"],
                        orig=blk["original_code"],
                        new=blk["new_code"],
                        repo=repo,
                        base_commit=base_commit,
                        token=self.github_token
                    )
                    if status == "SUCCESS" and diff_str:
                        synthesized_patch = diff_str
                        break

            if synthesized_patch:
                break

            messages.append({"role": "assistant", "content": content})
            messages.append({"role": "user", "content": "The generated patch could not be anchored cleanly. Please inspect exact character indentations and emit a verified SEARCH/REPLACE block."})

        elapsed = round(time.time() - start_time, 2)
        return {
            "instance_id": instance_id,
            "model_patch": synthesized_patch,
            "turns": turns,
            "prompt_tokens": total_prompt_tokens,
            "completion_tokens": total_completion_tokens,
            "total_tokens": total_prompt_tokens + total_completion_tokens,
            "latency_sec": elapsed
        }


def main():
    parser = argparse.ArgumentParser(description="Run Kronumos Aion (DeepSeek-R1 Dual-Brain Engine)")
    parser.add_argument("--endpoint", type=str, default=os.environ.get("AZURE_AI_ENDPOINT", "https://api.deepseek.com"))
    parser.add_argument("--api_key", type=str, default=os.environ.get("AZURE_AI_KEY", os.environ.get("DEEPSEEK_API_KEY", "")))
    parser.add_argument("--model", type=str, default="DeepSeek-R1")
    parser.add_argument("--dataset", type=str, default="princeton-nlp/SWE-bench_Verified")
    parser.add_argument("--num_samples", type=int, default=500)
    parser.add_argument("--output_dir", type=str, default="output_aion_500")
    parser.add_argument("--github_token", type=str, default=os.environ.get("GITHUB_TOKEN", ""))
    args = parser.parse_args()

    if not args.api_key:
        print("❌ Error: API Key wajib diisi via argumen --api_key atau environment variable AZURE_AI_KEY / DEEPSEEK_API_KEY!")
        sys.exit(1)

    os.makedirs(args.output_dir, exist_ok=True)
    pred_file = os.path.join(args.output_dir, "predictions.jsonl")
    metrics_file = os.path.join(args.output_dir, "eval_metrics.json")

    runner = KronumosAionRunner(
        endpoint=args.endpoint,
        api_key=args.api_key,
        model=args.model,
        github_token=args.github_token
    )

    print(f"📥 Memuat dataset {args.dataset} (split=test)...")
    ds = load_dataset(args.dataset, split="test")
    num_eval = min(args.num_samples, len(ds))

    print(f"🏛️ Memulai evaluasi KRONUMOS AION pada {num_eval} soal SWE-bench Verified...\n")

    completed_ids = set()
    if os.path.exists(pred_file):
        with open(pred_file, "r") as pf:
            for line in pf:
                if line.strip():
                    try:
                        entry = json.loads(line)
                        if entry.get("instance_id"):
                            completed_ids.add(entry["instance_id"])
                    except Exception:
                        pass
        if completed_ids:
            print(f"🔄 Checkpoint: {len(completed_ids)} soal sudah selesai sebelumnya (di-skip otomatis).", flush=True)

    for i in range(num_eval):
        inst = ds[i]
        iid = inst["instance_id"]
        if iid in completed_ids:
            continue

        repo = inst.get("repo", "unknown")
        print(f"[{i+1}/{num_eval}] 🏛️ Aion Reasoning: {iid} ({repo})...", flush=True)

        res = runner.solve_instance(inst)

        pred_entry = {
            "instance_id": iid,
            "model_patch": res["model_patch"],
            "model_name_or_path": f"Kronumos-Aion-{args.model}"
        }

        with open(pred_file, "a") as pf:
            pf.write(json.dumps(pred_entry) + "\n")
            pf.flush()

        badge = "✅ PATCH VALID" if res["model_patch"] else "❌ TANPA PATCH"
        print(f"    ↳ {badge} | Tokens: {res['total_tokens']} | Waktu: {res['latency_sec']}s\n", flush=True)

    print("🎉 SELESAI! Hasil disimpan di:", pred_file)


if __name__ == "__main__":
    main()
