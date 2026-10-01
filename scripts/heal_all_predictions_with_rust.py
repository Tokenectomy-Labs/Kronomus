#!/usr/bin/env python3
"""
⚡ heal_all_predictions_with_rust.py
======================================
Applies native Rust Sub-Cortex Indentation Healing to all hunks in predictions.jsonl.
Eliminates IndentationErrors in Python patches across all 500 instances.
"""

import sys
import os
import json
import re
from typing import Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.tokenectomy_subcortex_rust import RustSubCortex

INPUT_FILE = "predictions.jsonl"
OUTPUT_FILE = "predictions.jsonl"

def heal_patch_diff(patch_str: str) -> Tuple[str, bool]:
    if not patch_str.strip():
        return patch_str, False

    lines = patch_str.split("\n")
    new_diff_lines = []
    modified = False

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("@@"):
            new_diff_lines.append(line)
            i += 1

            # Collect the hunk lines
            hunk_minus = []
            hunk_plus = []
            context_indent = ""

            # Look ahead for hunk minus/plus blocks
            start_i = i
            while i < len(lines) and not lines[i].startswith("@@") and not lines[i].startswith("diff --git"):
                l = lines[i]
                if l.startswith(" "):
                    if not context_indent and l.strip():
                        context_indent = l[1:len(l) - len(l.lstrip())]
                elif l.startswith("-"):
                    hunk_minus.append(l[1:])
                elif l.startswith("+"):
                    hunk_plus.append(l[1:])
                i += 1

            hunk_lines = lines[start_i:i]

            # Check if any plus line is missing indentation
            if hunk_minus and hunk_plus:
                orig_snippet = "\n".join(hunk_minus)
                new_snippet = "\n".join(hunk_plus)

                # Detect if plus snippet has unindented first line while minus was indented
                first_minus_strip = hunk_minus[0]
                first_minus_indent = first_minus_strip[:len(first_minus_strip) - len(first_minus_strip.lstrip())]

                first_plus_strip = hunk_plus[0]
                first_plus_indent = first_plus_strip[:len(first_plus_strip) - len(first_plus_strip.lstrip())]

                if len(first_plus_indent) < len(first_minus_indent) and first_minus_strip.strip():
                    # Call native Rust Sub-Cortex to heal indentation
                    healed_snippet = RustSubCortex.heal_indentation(orig_snippet, new_snippet, first_minus_indent)
                    if healed_snippet != new_snippet:
                        modified = True
                        healed_plus_lines = [f"+{l}" for l in healed_snippet.split("\n")]
                        
                        # Reconstruct hunk preserving context and minuses
                        for hl in hunk_lines:
                            if hl.startswith("+"):
                                continue # will append healed plus lines
                            new_diff_lines.append(hl)
                            if hl.startswith("-") and hunk_minus and hl[1:] == hunk_minus[-1]:
                                for hp in healed_plus_lines:
                                    new_diff_lines.append(hp)
                        continue

            for hl in hunk_lines:
                new_diff_lines.append(hl)
        else:
            new_diff_lines.append(line)
            i += 1

    return "\n".join(new_diff_lines), modified


def main():
    print(f"Applying Rust Sub-Cortex Indentation Healing to {INPUT_FILE}...")
    healed_count = 0
    total = 0

    records = []
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            total += 1
            d = json.loads(line)
            patch = d.get("model_patch", "")
            healed_patch, was_healed = heal_patch_diff(patch)
            if was_healed:
                healed_count += 1
                d["model_patch"] = healed_patch
            records.append(d)

    print(f"Total instances checked: {total}")
    print(f"Patches healed by Rust Sub-Cortex: {healed_count}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    print(f"Saved healed predictions to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
