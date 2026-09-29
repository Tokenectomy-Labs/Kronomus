#!/usr/bin/env python3
"""
⚡ Kronumos 14B Kairos — Standalone Fine-Tuning Script
=====================================================
Usage:
  python3 scripts/train_kronumos_14b.py --target_train 5000 --target_val 1000 --epochs 2
"""

import os
import re
import json
import random
import argparse
from typing import Dict, Any, List, Set, Tuple

try:
    import torch
    from datasets import load_dataset, Dataset
    from trl import SFTTrainer
    from transformers import TrainingArguments, EarlyStoppingCallback
except ImportError:
    torch = None
    load_dataset = None
    Dataset = None
    SFTTrainer = None
    TrainingArguments = None
    EarlyStoppingCallback = None

try:
    from unsloth import FastLanguageModel, is_bfloat16_supported
    from unsloth.chat_templates import get_chat_template, train_on_responses_only
    UNSLOTH_AVAILABLE = True
except ImportError:
    UNSLOTH_AVAILABLE = False


KRONUMOS_SYSTEM_PROMPT = (
    "You are Kronumos Kairos v2, an autonomous bug-remediation engine natively integrated with "
    "the Tokenectomy M2M Sub-Cortex. You synthesize surgical, production-safe code fixes with zero dirty diffs.\n\n"
    "OPERATIONAL PROTOCOL:\n"
    "1. Always wrap your diagnostic analysis inside <thought>...</thought> tags before emitting code. "
    "Formulate: (a) Fault hypothesis from the Cleaned Technical Specification, (b) Verified repository target file and symbols, "
    "(c) Minimal defensive patch preserving full backward compatibility.\n"
    "2. NEVER modify code blocks tagged as [USER_REPRODUCTION_SNIPPET - REFERENCE ONLY, NEVER PATCH THIS]. "
    "Target ONLY real internal source files within the repository package tree.\n"
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


def parse_unified_diff(diff_text: str):
    files = re.findall(r"--- a/([^\s\n]+)", diff_text)
    if not files:
        files = re.findall(r"diff --git a/([^\s\n]+)", diff_text)
    if len(set(files)) != 1:
        return None
    fpath = files[0].strip()
    if any(fpath.endswith(ext) for ext in [".rst", ".md", ".txt", ".html", ".css", ".svg", ".png"]):
        return None
    if fpath.startswith("tests/") or "/tests/" in fpath or fpath.startswith("testing/"):
        return None
    orig_lines, new_lines = [], []
    in_hunk = False
    for line in diff_text.splitlines():
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
    if not orig_lines or not new_lines or len(orig_lines) > 50 or len(new_lines) > 50:
        return None
    return fpath, "\n".join(orig_lines), "\n".join(new_lines)


def load_dataset_pipeline(target_train: int, target_val: int):
    print("🔒 Loading protected SWE-bench Verified IDs...")
    sb_verified = load_dataset("princeton-nlp/SWE-bench_Verified", split="test")
    protected_ids = {x["instance_id"] for x in sb_verified}

    all_train = []
    if os.path.exists("dataset/kairos_v2_train.jsonl"):
        with open("dataset/kairos_v2_train.jsonl", "r", encoding="utf-8") as f:
            all_train = [json.loads(line) for line in f if line.strip()]

    all_val = []
    if os.path.exists("dataset/kairos_v2_val.jsonl"):
        with open("dataset/kairos_v2_val.jsonl", "r", encoding="utf-8") as f:
            all_val = [json.loads(line) for line in f if line.strip()]

    print(f"📦 Curated seed: {len(all_train)} train, {len(all_val)} val.")

    print("📥 Loading SWE-bench train split (19,008 rows)...")
    swe_train = load_dataset("princeton-nlp/SWE-bench", split="train")

    seen_ids = {s.get("instance_id", "") for s in all_train + all_val}
    new_candidates = []

    for item in swe_train:
        iid = item.get("instance_id", "")
        if iid in protected_ids or iid in seen_ids:
            continue
        prob = item.get("problem_statement", "")
        patch = item.get("patch", "")
        if not prob or not patch or len(prob) < 60:
            continue
        parsed = parse_unified_diff(patch)
        if not parsed:
            continue
        fpath, orig, new = parsed
        repo = item.get("repo", "")
        summary = prob.strip().splitlines()[0][:100]
        thought = (
            f"[Step 1: Anomaly & Target Symbol Diagnosis]\n"
            f"Target Component: `{fpath}`\n"
            f"Defect Vector: {summary}\n\n"
            f"[Step 2: Invariant Check & Defense]\n"
            f"Enforcing strict AST integrity, defensive boundary guards, and backward compatibility.\n\n"
            f"[Step 3: Surgical Mutation Execution]\n"
            f"Synthesizing atomic replacement block on `{fpath}`."
        )
        user_msg = f"Repository: {repo}\nIssue ID: {iid}\n\nProblem Description:\n{prob.strip()}"
        asst_msg = f"<thought>\n{thought}\n</thought>\n\nFile: {fpath}\n<<<<<<< SEARCH\n{orig.strip()}\n=======\n{new.strip()}\n>>>>>>> REPLACE"
        new_candidates.append({
            "instance_id": iid,
            "repo": repo,
            "messages": [
                {"role": "system", "content": KRONUMOS_SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
                {"role": "assistant", "content": asst_msg}
            ]
        })
        seen_ids.add(iid)

    print(f"✨ Mined {len(new_candidates)} surgical candidates.")
    random.seed(42)
    random.shuffle(new_candidates)

    needed_train = max(0, target_train - len(all_train))
    needed_val = max(0, target_val - len(all_val))

    final_train = all_train + new_candidates[:needed_train]
    final_val = all_val + new_candidates[needed_train:needed_train + needed_val]
    random.shuffle(final_train)
    random.shuffle(final_val)

    print(f"🎯 Scaled Train Dataset: {len(final_train)} instances")
    print(f"🎯 Scaled Val Dataset:   {len(final_val)} instances")
    return Dataset.from_list(final_train), Dataset.from_list(final_val)


def main():
    parser = argparse.ArgumentParser(description="Fine-tune Kronumos 14B on A100")
    parser.add_argument("--base_model", type=str, default="Qwen/Qwen2.5-Coder-14B-Instruct")
    parser.add_argument("--max_seq_len", type=int, default=8192)
    parser.add_argument("--target_train", type=int, default=5000)
    parser.add_argument("--target_val", type=int, default=1000)
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--batch_size", type=int, default=4)
    parser.add_argument("--grad_accum", type=int, default=4)
    parser.add_argument("--lr", type=float, default=1.5e-4)
    parser.add_argument("--output_dir", type=str, default="./kronumos_14b_checkpoints")
    args = parser.parse_args()

    if not UNSLOTH_AVAILABLE:
        raise RuntimeError("Unsloth is required. Install via pip install 'unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git'")

    print(f"🚀 Initializing FastLanguageModel: {args.base_model} (4-bit NF4)")
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=args.base_model,
        max_seq_length=args.max_seq_len,
        load_in_4bit=True,
        dtype=torch.bfloat16 if is_bfloat16_supported() else torch.float16,
    )

    print("⚡ Configuring LoRA with dropout=0.05...")
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_alpha=32,
        lora_dropout=0.05,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=42,
    )

    tokenizer = get_chat_template(
        tokenizer,
        chat_template="qwen-2.5",
        mapping={"role": "role", "content": "content", "user": "user", "assistant": "assistant"},
    )

    train_ds, val_ds = load_dataset_pipeline(args.target_train, args.target_val)

    def formatting_prompts_func(batch):
        convos = batch["messages"]
        texts = [tokenizer.apply_chat_template(convo, tokenize=False, add_generation_prompt=False) for convo in convos]
        return {"text": texts}

    train_ds = train_ds.map(formatting_prompts_func, batched=True)
    val_ds = val_ds.map(formatting_prompts_func, batched=True)

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        dataset_text_field="text",
        max_seq_length=args.max_seq_len,
        dataset_num_proc=2,
        packing=False,
        args=TrainingArguments(
            per_device_train_batch_size=args.batch_size,
            gradient_accumulation_steps=args.grad_accum,
            warmup_ratio=0.05,
            num_train_epochs=args.epochs,
            learning_rate=args.lr,
            fp16=not is_bfloat16_supported(),
            bf16=is_bfloat16_supported(),
            logging_steps=10,
            eval_strategy="steps",
            eval_steps=50,
            save_strategy="steps",
            save_steps=50,
            load_best_model_at_end=True,
            metric_for_best_model="eval_loss",
            greater_is_better=False,
            optim="paged_adamw_8bit",
            weight_decay=0.05,
            lr_scheduler_type="cosine",
            seed=42,
            output_dir=args.output_dir,
            save_total_limit=2,
            report_to="none"
        ),
        callbacks=[EarlyStoppingCallback(early_stopping_patience=3)],
    )

    trainer = train_on_responses_only(
        trainer,
        instruction_part="<|im_start|>user\n",
        response_part="<|im_start|>assistant\n",
    )

    print("⚡ Starting training loop on NVIDIA A100...")
    trainer.train()

    # Save and export
    lora_dir = "./kronumos_14b_kairos_lora"
    merged_dir = "./kronumos_14b_kairos_merged_16bit"
    gguf_dir = "./kronumos_14b_gguf"

    model.save_pretrained(lora_dir)
    tokenizer.save_pretrained(lora_dir)
    print(f"💾 LoRA adapter saved to {lora_dir}")

    print("🔄 Merging weights into 16-bit...")
    model.save_pretrained_merged(merged_dir, tokenizer, save_method="merged_16bit")
    print(f"💾 Merged model saved to {merged_dir}")

    print("📦 Exporting to GGUF Q4_K_M...")
    model.save_pretrained_gguf(gguf_dir, tokenizer, quantization_method="q4_k_m")
    print(f"✅ GGUF exported to {gguf_dir}")


if __name__ == "__main__":
    main()
