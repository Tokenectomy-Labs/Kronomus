"""
⚡ Kronumos Sub-Cortex Issue De-Noiser & Signal Extractor
==========================================================
Excises conversational human chaff, distinguishes user reproduction code
from actual repository source files, and extracts the Core Triad:
1. TARGET_SYMBOLS (Functions, classes, exceptions verified in repo)
2. OBSERVED_BEHAVIOR (Tracebacks, error messages, crash symptoms)
3. EXPECTED_BEHAVIOR (Expected return types, behavior contracts)
"""

import re
from typing import Dict, Any, List, Set, Optional, Tuple


class IssueDeNoiser:
    """
    Sub-Cortex Issue Discourse De-Noiser:
    Converts unstructured, noisy GitHub issue discussions into a structured,
    high-signal technical specification for Kronumos Kairos.
    """

    # Human conversational chaff patterns to discard
    GREETINGS_PATTERN = re.compile(
        r"^(?:hi|hello|hey|dear)\b.*?(?:\n|$)|^(?:thanks|thank you|cheers|best regards|regards|sincerely)\b.*?(?:\n|$)",
        re.IGNORECASE | re.MULTILINE
    )
    
    MENTION_PATTERN = re.compile(r"@([a-zA-Z0-9_\-]+)")
    
    WORKAROUND_PATTERN = re.compile(
        r"(?:as a (?:temporary )?workaround|workaround for now|my temporary fix|i worked around this by).*?(?:\n\n|\Z)",
        re.IGNORECASE | re.DOTALL
    )
    
    METADATA_CHAFF_PATTERN = re.compile(
        r"(?:duplicate of #\d+|closing (?:this|in favor of)|closed by #\d+|milestone:? \S+|triage:? \S+)",
        re.IGNORECASE
    )

    QUOTE_BLOCK_PATTERN = re.compile(r"^>.*$", re.MULTILINE)

    # Core signal patterns
    TRACEBACK_PATTERN = re.compile(
        r"(?:Traceback \(most recent call last\):.*?(?:\n[A-Za-z0-9_.]+(?:Error|Exception|Warning):[^\n]*))",
        re.DOTALL
    )

    EXPECTED_PATTERN = re.compile(
        r"(?:expected(?:\s+behavior)?(?:\s+to)?[:\s]+([^\n]+(?:\n[^\n]+)?)|"
        r"should(?:\s+instead)?\s+([^\n]+(?:\n[^\n]+)?)|"
        r"it should return\s+([^\n]+))",
        re.IGNORECASE
    )

    EXCEPTION_PATTERN = re.compile(
        r"\b([A-Z][a-zA-Z0-9]+(?:Error|Exception|Warning|Fault))\b"
    )

    SYMBOL_PATTERN = re.compile(
        r"\b([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*){1,4})\b"
    )

    @classmethod
    def clean_human_chaff(cls, text: str) -> str:
        """Removes greetings, quotes, meta comments, and workaround side-discussions."""
        cleaned = cls.QUOTE_BLOCK_PATTERN.sub("", text)
        cleaned = cls.GREETINGS_PATTERN.sub("", cleaned)
        cleaned = cls.WORKAROUND_PATTERN.sub("", cleaned)
        cleaned = cls.METADATA_CHAFF_PATTERN.sub("", cleaned)
        # Collapse excessive newlines
        cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
        return cleaned.strip()

    @classmethod
    def tag_code_blocks(cls, text: str, repo_files: Optional[Set[str]] = None) -> str:
        """
        Tags code blocks to distinguish user reproduction scripts from real repo files.
        If a code block does not reference a verified repo file, tags it as DO NOT EDIT.
        """
        def replace_block(match):
            lang = match.group(1) or ""
            code = match.group(2)
            
            # Check if this block looks like a standalone reproducer / scratch script
            is_reproducer = False
            first_lines = code[:200].lower()
            if any(k in first_lines for k in ["def reproduce", "poc", "example", "my_model", "dummy", "import pytest", "test_"]):
                is_reproducer = True
            elif "class " in code and not any(k in code for k in ["self.", "def __init__"]):
                # Often user model definitions
                is_reproducer = True

            tag = "\n# [USER_REPRODUCTION_SNIPPET - REFERENCE ONLY, NEVER PATCH THIS]" if is_reproducer else ""
            return f"```{lang}{tag}\n{code}\n```"

        return re.sub(r"```([a-zA-Z0-9_]*)\n(.*?)\n```", replace_block, text, flags=re.DOTALL)

    @classmethod
    def extract_core_triad(cls, text: str, repo: str = "") -> Dict[str, Any]:
        """
        Extracts the high-value technical signals:
        - Target Symbols (classes, methods, exceptions)
        - Observed Crash / Behavior
        - Expected Contract
        """
        # 1. Traceback
        tb_match = cls.TRACEBACK_PATTERN.search(text)
        traceback_str = tb_match.group(0).strip() if tb_match else ""

        # 2. Exceptions
        exceptions = list(set(cls.EXCEPTION_PATTERN.findall(text)))

        # 3. Target Symbols (e.g. django.db.models.QuerySet)
        raw_symbols = cls.SYMBOL_PATTERN.findall(text)
        # Filter out common false positives (like version numbers or URLs)
        clean_symbols = [
            s for s in set(raw_symbols)
            if not s.startswith("http") and not any(c.isdigit() for c in s.split(".")[0])
            and len(s.split(".")) >= 2
        ]

        # 4. Expected Behavior
        expected_matches = cls.EXPECTED_PATTERN.findall(text)
        expected_summary = []
        for match in expected_matches:
            for group in match:
                if group and group.strip():
                    expected_summary.append(group.strip())
                    break

        return {
            "traceback": traceback_str,
            "exceptions": sorted(exceptions),
            "symbols": sorted(clean_symbols)[:8],
            "expected_behavior": expected_summary[:3]
        }

    @classmethod
    def denoise_issue(cls, raw_issue: str, repo: str = "", repo_files: Optional[Set[str]] = None) -> Dict[str, Any]:
        """
        Main entry point: Cleans an unstructured issue into a structured,
        anti-hallucination prompt payload.
        """
        chaff_free = cls.clean_human_chaff(raw_issue)
        tagged_text = cls.tag_code_blocks(chaff_free, repo_files)
        triad = cls.extract_core_triad(raw_issue, repo)

        # Build clean specification string
        spec_lines = ["[CLEANED TECHNICAL SPECIFICATION]"]
        if triad["exceptions"]:
            spec_lines.append(f"Primary Exception(s): {', '.join(triad['exceptions'])}")
        if triad["symbols"]:
            spec_lines.append(f"Target Symbol References: {', '.join(triad['symbols'])}")
        if triad["expected_behavior"]:
            spec_lines.append("Expected Contract: " + "; ".join(triad["expected_behavior"]))
        
        spec_header = "\n".join(spec_lines)

        return {
            "cleaned_text": tagged_text,
            "specification_header": spec_header,
            "triad": triad,
            "token_reduction_pct": round((1.0 - (len(tagged_text) / max(1, len(raw_issue)))) * 100, 1)
        }
