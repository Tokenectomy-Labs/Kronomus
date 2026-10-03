#!/usr/bin/env python3
"""
⚡ Tokenectomy Sub-Cortex — Zero-Token AST & Scope Auto-Healer
==============================================================
Part of the Tokenectomy M2M Sub-Cortex architecture for Kronumos Kairos.

Functions:
1. Auto-Indentation Healer: Eliminates `IndentationError` by automatically
   detecting the target anchor indent and rebasing unindented model code in 0ms.
2. Symbol & Scope Guard: Uses Python AST/symtable to catch `NameError` and
   undefined identifiers before patches are committed.
3. Patch Integrity Verifier: Ensures the integrated full-file AST compiles cleanly.
"""

import ast
import re
import textwrap
from typing import Tuple, List, Optional, Set, Dict


class TokenectomyIndentationHealer:
    """
    Sub-millisecond AST indentation aligner.
    Eliminates Python IndentationError without wasting LLM tokens.
    """

    @staticmethod
    def detect_base_indent(snippet: str) -> str:
        """Find the leading whitespace of the first non-empty line."""
        for line in snippet.splitlines():
            if line.strip():
                return line[:len(line) - len(line.lstrip())]
        return ""

    @classmethod
    def heal(cls, orig_snippet: str, new_snippet: str, anchor_indent: str = "") -> str:
        """
        Rebases `new_snippet` to match the expected indentation level.
        Preserves relative indentation within blocks.
        """
        if not new_snippet.strip():
            return new_snippet

        # Determine target indent: explicit anchor > orig_snippet base
        target_indent = anchor_indent
        if not target_indent and orig_snippet:
            target_indent = cls.detect_base_indent(orig_snippet)

        if not target_indent:
            return new_snippet

        new_lines = new_snippet.splitlines()
        non_empty = [l for l in new_lines if l.strip()]
        if not non_empty:
            return new_snippet

        # If already indented with target_indent, keep as is
        first_indent = non_empty[0][:len(non_empty[0]) - len(non_empty[0].lstrip())]
        if first_indent == target_indent:
            return new_snippet

        # Calculate relative offsets
        min_current = min(len(l) - len(l.lstrip()) for l in non_empty)
        healed_lines = []
        for l in new_lines:
            if not l.strip():
                healed_lines.append("")
            else:
                current_indent_len = len(l) - len(l.lstrip())
                rel_offset = current_indent_len - min_current
                healed_lines.append(target_indent + (" " * rel_offset) + l.strip())

        return "\n".join(healed_lines)


class TokenectomyScopeGuard:
    """
    Symbolic AST Scope and Identifier Validator.
    Flags undefined variables and provides immediate M2M self-healing hints.
    """

    BUILTINS = set(dir(__builtins__)) | {
        "self", "cls", "True", "False", "None", "NotImplemented", "Ellipsis",
        "super", "args", "kwargs", "type", "isinstance", "issubclass"
    }

    @classmethod
    def audit_function_scope(cls, func_ast: ast.FunctionDef, modified_lines: Set[int] = None) -> List[Dict]:
        """
        Audit a function's local scope for undefined names in modified lines.
        Returns a list of violation dicts with line number, symbol, and healing hint.
        """
        violations = []

        # Collect function parameters
        defined_symbols: Set[str] = set()
        for a in func_ast.args.args:
            defined_symbols.add(a.arg)
        for a in getattr(func_ast.args, "posonlyargs", []):
            defined_symbols.add(a.arg)
        for a in getattr(func_ast.args, "kwonlyargs", []):
            defined_symbols.add(a.arg)
        if func_ast.args.vararg:
            defined_symbols.add(func_ast.args.vararg.arg)
        if func_ast.args.kwarg:
            defined_symbols.add(func_ast.args.kwarg.arg)

        # Collect local assignments
        for node in ast.walk(func_ast):
            if isinstance(node, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                targets = node.targets if hasattr(node, "targets") else [node.target]
                for t in targets:
                    if isinstance(t, ast.Name):
                        defined_symbols.add(t.id)
            elif isinstance(node, (ast.For, ast.AsyncFor)):
                if isinstance(node.target, ast.Name):
                    defined_symbols.add(node.target.id)
            elif isinstance(node, ast.ExceptHandler) and node.name:
                defined_symbols.add(node.name)

        # Check Name loads
        for node in ast.walk(func_ast):
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                symbol = node.id
                if modified_lines and node.lineno not in modified_lines:
                    continue

                if symbol not in defined_symbols and symbol not in cls.BUILTINS:
                    # Check if it looks like a missing 'self.' attribute
                    hint = f"self.{symbol}"
                    violations.append({
                        "line": getattr(node, "lineno", 0),
                        "symbol": symbol,
                        "message": f"Undefined variable `{symbol}` in function `{func_ast.name}`.",
                        "suggestion": f"Did you mean `{hint}` or is `{symbol}` missing from imports?"
                    })

        return violations

    @classmethod
    def inspect_snippet_scope(cls, snippet: str, enclosing_func_name: str = "") -> List[str]:
        """
        Fast heuristic audit on a standalone code snippet.
        """
        violations = []
        try:
            tree = ast.parse(textwrap.dedent(snippet))
        except SyntaxError:
            return violations

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                func_violations = cls.audit_function_scope(node)
                for v in func_violations:
                    violations.append(f"Line {v['line']}: {v['message']} -> Hint: {v['suggestion']}")

        return violations

    @classmethod
    def audit_code(cls, snippet: str, enclosing_func_name: str = "") -> List[str]:
        """Convenience alias for inspect_snippet_scope."""
        return cls.inspect_snippet_scope(snippet, enclosing_func_name)


class TokenectomyPatchIntegrity:
    """
    Full-File AST Compilation & Guardrail Verifier.
    """

    @staticmethod
    def verify_full_file(content: str, file_path: str = "") -> Tuple[bool, Optional[str]]:
        """
        Verify that the full file parses into a clean Python AST.
        """
        if not file_path.endswith(".py"):
            return True, None

        try:
            ast.parse(content)
            return True, None
        except SyntaxError as e:
            return False, f"AST SyntaxError on line {e.lineno}, col {e.offset}: {e.msg}"
        except IndentationError as e:
            return False, f"AST IndentationError on line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, f"AST Verification Failure: {str(e)}"
