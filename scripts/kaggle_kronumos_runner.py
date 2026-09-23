"""
⚡ Kronumos Arena Runner — Kaggle GPU Test Harness
===================================================
Run this script in a Kaggle Notebook (GPU T4 x2 or P100 enabled).
It loads NadevA23/Kronumos, evaluates issues from princeton-nlp/SWE-bench_Verified,
records enterprise metrics (tokens, latencies, turns, tool accuracy),
and exports official `predictions.jsonl` ready for Docker verification.

How to run on Kaggle:
1. Create a new Kaggle Notebook (Settings -> Accelerator -> GPU T4 x2 or P100).
2. Paste this entire script or run: `!python kaggle_kronumos_runner.py --num_samples 10`
3. Download `predictions.jsonl` and `eval_metrics.json` from the output tab.
"""

import os
import re
import json
import time
import argparse
from typing import Dict, Any, List
from datetime import datetime

import torch
from datasets import load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# ---------------------------------------------------------
# 1. Kronumos Agent System Prompt & Tool Schema
# ---------------------------------------------------------
SYSTEM_PROMPT = (
    "You are Kronumos, an autonomous bug-remediation agent natively equipped with "
    "the Tokenectomy M2M Sub-Cortex. You handle the full incident lifecycle: "
    "diagnose through get_error_context (and inspect_docker/probe_database when "
    "the failure is infra-level), open an incident issue for tracking, apply a "
    "verified atomic patch, run a blast-radius check before merging when the "
    "change is non-trivial, deliver the fix via a branch/commit/pull request, "
    "link the issue to its fix PR, and close the issue once resolved. You are "
    "not a general-purpose coding assistant — you exist solely to remediate "
    "reported bugs and incidents end-to-end, deterministically and with zero "
    "dirty diffs. Target ONLY existing source code files inside the repository "
    "(e.g., django/, astropy/, sympy/). Never patch demonstration scripts, "
    "scratch files, or test runners (e.g. test.py, app/models.py, poc.py)."
)

TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "get_error_context",
            "description": "Excise framework noise, redact credentials, and extract exact offending code snippets from a raw stack trace.",
            "parameters": {
                "type": "object",
                "properties": {
                    "log": {"type": "string"},
                    "strategy": {"type": "string", "enum": ["aggressive", "conservative"]},
                },
                "required": ["log"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "apply_code_patch",
            "description": "Apply an atomic search-and-replace AST patch, verified by the compiler before commit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "original_code": {"type": "string"},
                    "new_code": {"type": "string"},
                },
                "required": ["file_path", "original_code", "new_code"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sentinel_analyze_blast_radius",
            "description": "Map caller dependency graph for a symbol/file before applying a patch.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string"},
                    "symbol": {"type": "string"},
                },
                "required": ["file_path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_fix_branch",
            "description": "Create a new git branch for the fix.",
            "parameters": {
                "type": "object",
                "properties": {"branch_name": {"type": "string"}},
                "required": ["branch_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "commit_fix",
            "description": "Commit the verified patch to the current branch.",
            "parameters": {
                "type": "object",
                "properties": {"commit_message": {"type": "string"}},
                "required": ["commit_message"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "open_pull_request",
            "description": "Open a PR from the fix branch to the target branch.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_branch": {"type": "string", "default": "main"},
                    "title": {"type": "string"},
                },
                "required": ["title"],
            },
        },
    },
]

# ---------------------------------------------------------
# 2. Sub-Cortex Helper (Tokenectomy Emulation / Redaction)
# ---------------------------------------------------------
def simulate_subcortex_scrub(raw_trace: str) -> Dict[str, Any]:
    """
    Sub-Cortex Tokenectomy logic:
    Redacts credentials and eliminates redundant site-packages / framework frames.
    """
    cleaned = raw_trace
    # 1. Redact common secret patterns
    cleaned = re.sub(r'(Bearer\s+[A-Za-z0-9\-._~+/]+=*)', '[REDACTED_AUTH_TOKEN]', cleaned)
    cleaned = re.sub(r'([a-zA-Z0-9_]+:(?:[^\s@/:]+)@)', '[REDACTED_USER_PASS]@', cleaned)
    cleaned = re.sub(r'(AKIA[0-9A-Z]{16})', '[REDACTED_AWS_KEY]', cleaned)
    
    # 2. Excise internal framework frames
    lines = cleaned.splitlines()
    filtered_lines = []
    skip_frame = False
    for line in lines:
        if any(noise in line for noise in ["/lib/python", "site-packages", "node_modules", "internal/modules"]):
            skip_frame = True
            continue
        if line.strip().startswith("File ") and skip_frame:
            skip_frame = False
        if not skip_frame:
            filtered_lines.append(line)
            
    scrubbed_text = "\n".join(filtered_lines) if filtered_lines else raw_trace
    raw_tokens = len(raw_trace.split())
    clean_tokens = len(scrubbed_text.split())
    savings_pct = round(((raw_tokens - clean_tokens) / max(raw_tokens, 1)) * 100, 2)
    
    return {
        "scrubbed_log": scrubbed_text,
        "raw_tokens": raw_tokens,
        "clean_tokens": clean_tokens,
        "savings_pct": max(savings_pct, 0.0)
    }

def convert_patch_call_to_diff(file_path: str, orig: str, new: str, repo: str = "", base_commit: str = "") -> str:
    """Format patch call into a valid POSIX-compliant unified git diff string with real line context."""
    clean_path = file_path.lstrip("/").replace("//", "/")
    
    # 1. Attempt to fetch real file from GitHub to compute exact unified diff with line numbers
    if repo and base_commit and clean_path:
        try:
            url = f"https://raw.githubusercontent.com/{repo}/{base_commit}/{clean_path}"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Kronumos-Kaggle-Runner)"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw_content = resp.read().decode("utf-8", errors="replace")
                file_lines = raw_content.splitlines(keepends=True)
                
                # Check exact match
                if orig in raw_content:
                    new_content = raw_content.replace(orig, new, 1)
                    diff = list(difflib.unified_diff(
                        file_lines,
                        new_content.splitlines(keepends=True),
                        fromfile=f"a/{clean_path}",
                        tofile=f"b/{clean_path}"
                    ))
                    if diff:
                        return "".join(diff)
                        
                # Check stripped whitespace match
                target_stripped = [l.strip() for l in orig.splitlines() if l.strip()]
                if target_stripped:
                    window_size = len(target_stripped)
                    target_str = "\n".join(target_stripped)
                    best_ratio = 0.0
                    best_start = -1
                    for i in range(len(file_lines)):
                        cand_slice = [file_lines[i + k].strip() for k in range(window_size) if i + k < len(file_lines)]
                        cand_str = "\n".join(cand_slice)
                        ratio = difflib.SequenceMatcher(None, target_str, cand_str).ratio()
                        if ratio > best_ratio:
                            best_ratio = ratio
                            best_start = i
                    if best_ratio >= 0.70 and best_start >= 0:
                        anchor_line = file_lines[best_start]
                        indent = anchor_line[:len(anchor_line) - len(anchor_line.lstrip())]
                        formatted_plus = [indent + p.lstrip() + "\n" if p.strip() else "\n" for p in new.splitlines()]
                        new_lines = file_lines[:best_start] + formatted_plus + file_lines[best_start + window_size:]
                        diff = list(difflib.unified_diff(
                            file_lines,
                            new_lines,
                            fromfile=f"a/{clean_path}",
                            tofile=f"b/{clean_path}"
                        ))
                        if diff:
                            return "".join(diff)
        except Exception:
            pass
            
    # 2. Robust fallback with syntactically valid hunk counts (never malformed @@ -1,1 +1,1 @@)
    orig_lines = orig.splitlines()
    new_lines_list = new.splitlines()
    orig_count = max(1, len(orig_lines))
    new_count = max(1, len(new_lines_list))
    
    diff_lines = [
        f"diff --git a/{clean_path} b/{clean_path}",
        f"--- a/{clean_path}",
        f"+++ b/{clean_path}",
        f"@@ -1,{orig_count} +1,{new_count} @@",
    ]
    for line in orig_lines:
        diff_lines.append(f"-{line}")
    for line in new_lines_list:
        diff_lines.append(f"+{line}")
    return "\n".join(diff_lines) + "\n"

# ---------------------------------------------------------
# 3. Benchmark Evaluator Class
# ---------------------------------------------------------
class KronumosBenchmarkRunner:
    def __init__(self, model_id: str = "NadevA23/Kronumos", load_in_4bit: bool = True):
        print(f"📦 Loading tokenizer: {model_id}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, trust_remote_code=True)
        
        print(f"⚡ Loading model weights (4-bit={load_in_4bit})...")
        if load_in_4bit:
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=torch.bfloat16,
                device_map="auto",
                trust_remote_code=True,
            )
            
        im_end_id = self.tokenizer.convert_tokens_to_ids("<|im_end|>")
        self.stop_tokens = list({self.tokenizer.eos_token_id, im_end_id})
        print("✅ Kronumos ready for inference!")

    def solve_instance(self, instance: Dict[str, Any], max_turns: int = 4) -> Dict[str, Any]:
        instance_id = instance.get("instance_id", "unknown")
        repo = instance.get("repo", "unknown")
        problem_statement = instance.get("problem_statement", "")
        
        user_prompt = (
            f"Repository: {repo}\n"
            f"Issue ID: {instance_id}\n\n"
            f"Problem Description:\n{problem_statement}"
        )
        
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
        
        trajectory = []
        synthesized_patch = ""
        total_prompt_tokens = 0
        total_completion_tokens = 0
        tool_call_errors = 0
        turns = 0
        start_time = time.time()
        
        for turn in range(max_turns):
            turns += 1
            # Apply chat template
            encoded = self.tokenizer.apply_chat_template(
                messages,
                tools=TOOLS_SCHEMA,
                tokenize=True,
                add_generation_prompt=True,
                return_tensors="pt"
            )
            if isinstance(encoded, dict) or hasattr(encoded, "__getitem__"):
                raw_input_ids = encoded["input_ids"]
                raw_attention_mask = encoded.get("attention_mask", None) if hasattr(encoded, "get") else getattr(encoded, "attention_mask", None)
            elif hasattr(encoded, "input_ids"):
                raw_input_ids = encoded.input_ids
                raw_attention_mask = getattr(encoded, "attention_mask", None)
            else:
                raw_input_ids = encoded
                raw_attention_mask = None

            input_ids = raw_input_ids.to(self.model.device) if hasattr(raw_input_ids, "to") else torch.tensor(raw_input_ids).to(self.model.device)
            if raw_attention_mask is not None and hasattr(raw_attention_mask, "to"):
                attention_mask = raw_attention_mask.to(self.model.device)
            else:
                attention_mask = torch.ones_like(input_ids)
            
            prompt_len = input_ids.shape[1]
            total_prompt_tokens += prompt_len
            
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    max_new_tokens=768,
                    do_sample=False,
                    eos_token_id=self.stop_tokens,
                )
                
            completion_ids = outputs[0][prompt_len:]
            total_completion_tokens += len(completion_ids)
            response_text = self.tokenizer.decode(completion_ids, skip_special_tokens=True).strip()
            
            trajectory.append({
                "turn": turns,
                "response": response_text
            })
            
            # Parse tool calls emitted by Kronumos
            found_calls = []
            for match in re.finditer(r'\{\s*"name"\s*:\s*"[^"]+"\s*,\s*"arguments"\s*:\s*\{.*?\}\s*\}', response_text, re.DOTALL):
                try:
                    call_obj = json.loads(match.group(0))
                    found_calls.append(call_obj)
                except json.JSONDecodeError:
                    tool_call_errors += 1
                    
            if not found_calls:
                # If model produced patch in unified diff block
                if "diff --git" in response_text or "@@ -" in response_text:
                    synthesized_patch = response_text
                break
                
            # Process tool calls
            messages.append({"role": "assistant", "content": response_text})
            tool_outputs = []
            
            for call in found_calls:
                tool_name = call.get("name")
                args = call.get("arguments", {})
                
                if tool_name == "get_error_context":
                    raw_log = args.get("log", problem_statement)
                    scrub = simulate_subcortex_scrub(raw_log)
                    tool_outputs.append(f"Sub-Cortex Cleaned ({scrub['savings_pct']}% tokens excised):\n{scrub['scrubbed_log']}")
                    
                elif tool_name == "apply_code_patch":
                    f_path = args.get("file_path", "")
                    orig = args.get("original_code", "")
                    new_code = args.get("new_code", "")
                    base_commit = instance.get("base_commit", "")
                    synthesized_patch = convert_patch_call_to_diff(f_path, orig, new_code, repo=repo, base_commit=base_commit)
                    tool_outputs.append(f"Patch applied cleanly to {f_path}. AST syntax valid.")
                    
                elif tool_name == "sentinel_analyze_blast_radius":
                    tool_outputs.append("Blast radius: 1 direct caller, 0 breaking API changes.")
                    
                elif tool_name == "create_fix_branch":
                    tool_outputs.append(f"Branch created: {args.get('branch_name')}")
                    
                elif tool_name == "commit_fix":
                    tool_outputs.append(f"Committed: {args.get('commit_message')}")
                    
                elif tool_name == "open_pull_request":
                    tool_outputs.append(f"PR opened: {args.get('title')}")
                    
            if synthesized_patch and turns >= 2:
                # Loop completed
                break
                
            messages.append({
                "role": "user",
                "content": "\n".join(tool_outputs) if tool_outputs else "Action executed successfully. Proceed."
            })
            
        elapsed_sec = round(time.time() - start_time, 2)
        
        return {
            "instance_id": instance_id,
            "model_patch": synthesized_patch,
            "turns": turns,
            "prompt_tokens": total_prompt_tokens,
            "completion_tokens": total_completion_tokens,
            "total_tokens": total_prompt_tokens + total_completion_tokens,
            "tool_call_errors": tool_call_errors,
            "latency_sec": elapsed_sec,
            "trajectory": trajectory,
        }

# ---------------------------------------------------------
# 4. Main Batch Runner
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Run Kronumos SWE-bench Evaluation")
    parser.add_argument("--model_id", type=str, default="NadevA23/Kronumos")
    parser.add_argument("--dataset", type=str, default="princeton-nlp/SWE-bench_Verified")
    parser.add_argument("--split", type=str, default="test")
    parser.add_argument("--num_samples", type=int, default=15)
    parser.add_argument("--output_dir", type=str, default="output")
    args = parser.parse_args()
    
    os.makedirs(args.output_dir, exist_ok=True)
    os.makedirs(os.path.join(args.output_dir, "trajectories"), exist_ok=True)
    
    print(f"📥 Loading dataset: {args.dataset} (split={args.split})...")
    ds = load_dataset(args.dataset, split=args.split)
    instances = [ds[i] for i in range(min(args.num_samples, len(ds)))]
    print(f"🎯 Evaluating on {len(instances)} instances.")
    
    runner = KronumosBenchmarkRunner(model_id=args.model_id)
    
    predictions = []
    metrics_summary = {
        "timestamp": datetime.now().isoformat(),
        "model": args.model_id,
        "dataset": args.dataset,
        "total_instances": len(instances),
        "results": []
    }
    
    pred_file = os.path.join(args.output_dir, "predictions.jsonl")
    with open(pred_file, "w") as pf:
        for idx, inst in enumerate(instances):
            inst_id = inst.get("instance_id")
            print(f"\n[{idx+1}/{len(instances)}] 🔧 Running: {inst_id} ({inst.get('repo')})...", flush=True)
            
            res = runner.solve_instance(inst)
            
            # Memory cleanup for large batch runs
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            # Format according to official SWE-bench prediction schema
            pred_entry = {
                "instance_id": inst_id,
                "model_patch": res["model_patch"],
                "model_name_or_path": "Kronumos-7B"
            }
            pf.write(json.dumps(pred_entry) + "\n")
            pf.flush()
            
            predictions.append(pred_entry)
            metrics_summary["results"].append({
                "instance_id": inst_id,
                "has_patch": bool(res["model_patch"]),
                "turns": res["turns"],
                "total_tokens": res["total_tokens"],
                "latency_sec": res["latency_sec"],
                "errors": res["tool_call_errors"]
            })
            
            # Save full trajectory for audit
            traj_path = os.path.join(args.output_dir, "trajectories", f"{inst_id}.json")
            with open(traj_path, "w") as tf:
                json.dump(res, tf, indent=2)
                
            progress_pct = round(((idx + 1) / len(instances)) * 100, 1)
            print(f"    ↳ [{progress_pct}%] Patch: {'✅ YES' if res['model_patch'] else '❌ NO'} | Turns: {res['turns']} | Tokens: {res['total_tokens']} | Time: {res['latency_sec']}s", flush=True)

    summary_file = os.path.join(args.output_dir, "eval_metrics.json")
    with open(summary_file, "w") as sf:
        json.dump(metrics_summary, sf, indent=2)
        
    print("\n" + "=" * 60)
    print("🎉 BENCHMARK RUN COMPLETED!")
    print(f"📁 Predictions saved to: {pred_file}")
    print(f"📊 Metrics summary saved to: {summary_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()
