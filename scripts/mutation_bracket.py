"""
⚡ Zero-LLM Deterministic Mutation Bracket (APR Engine)
======================================================
Automated rule-based Program Repair (APR) operators to heal
near-miss boundary, off-by-one, and None-check conditions in 0 tokens (<5ms).
"""

import ast
import re
import textwrap
from typing import List, Tuple, Optional


class ZeroLLMMutationBracket:
    """
    Applies deterministic AST/token mutation operators to candidate code patches.
    Resolves trivial near-miss defects without invoking expensive LLM inference.
    """

    OPERATORS = [
        # 1. Boundary Condition Flips
        ("boundary_flip", r"(\b[a-zA-Z0-9_.]+\s*)(>)(?!=)(\s*[a-zA-Z0-9_.]+)", r"\1>=\3"),
        ("boundary_flip", r"(\b[a-zA-Z0-9_.]+\s*)(<)(?!=)(\s*[a-zA-Z0-9_.]+)", r"\1<=\3"),
        ("boundary_flip", r"(\b[a-zA-Z0-9_.]+\s*)(>=)(\s*[a-zA-Z0-9_.]+)", r"\1>\3"),
        ("boundary_flip", r"(\b[a-zA-Z0-9_.]+\s*)(<=)(\s*[a-zA-Z0-9_.]+)", r"\1<\3"),
        ("equality_flip", r"(\b[a-zA-Z0-9_.]+\s*)(==)(\s*[a-zA-Z0-9_.]+)", r"\1!=\3"),

        # 2. Off-by-one Adjustments
        ("off_by_one_add", r"(\b[a-zA-Z0-9_.]+\s*)\+\s*1\b", r"\1- 1"),
        ("off_by_one_sub", r"(\b[a-zA-Z0-9_.]+\s*)-\s*1\b", r"\1+ 1"),
        ("len_off_by_one", r"len\(([a-zA-Z0-9_.]+)\)", r"len(\1) - 1"),

        # 3. None-Safety Guards (Qi et al. defensive repair)
        ("none_check_explicit", r"\bif\s+([a-zA-Z0-9_.]+):", r"if \1 is not None:"),
        ("none_check_negative", r"\bif\s+not\s+([a-zA-Z0-9_.]+):", r"if \1 is None:"),

        # 4. Container Type Discrepancies
        ("list_to_tuple", r"return\s+list\(([^)]+)\)", r"return tuple(\1)"),
        ("tuple_to_list", r"return\s+tuple\(([^)]+)\)", r"return list(\1)"),
    ]

    @classmethod
    def generate_candidate_mutations(cls, code_snippet: str) -> List[Tuple[str, str]]:
        """
        Generates a list of (operator_name, mutated_code) pairs.
        Each mutation is guaranteed to be syntactically valid Python.
        """
        candidates = []
        seen = {code_snippet.strip()}

        for op_name, pattern, replacement in cls.OPERATORS:
            if re.search(pattern, code_snippet):
                mutated = re.sub(pattern, replacement, code_snippet, count=1)
                if mutated.strip() not in seen:
                    seen.add(mutated.strip())
                    # Validate AST syntax integrity
                    try:
                        ast.parse(textwrap.dedent(mutated))
                        candidates.append((op_name, mutated))
                    except SyntaxError:
                        pass

        return candidates

    @classmethod
    def synthesize_search_replace_bracket(cls, file_path: str, original: str, base_candidate: str) -> List[Tuple[str, str]]:
        """
        Takes an existing SEARCH/REPLACE replacement block and generates
        a bracket of deterministic near-miss variations.
        """
        variations = cls.generate_candidate_mutations(base_candidate)
        bracket_blocks = []

        for op_name, mutated_code in variations:
            block = (
                f"File: {file_path}\n"
                f"<<<<<<< SEARCH\n{original}\n=======\n{mutated_code}\n>>>>>>> REPLACE"
            )
            bracket_blocks.append((op_name, block))

        return bracket_blocks
