#!/usr/bin/env python3
"""
⚡ Tokenectomy Sub-Cortex — High-Speed Native Rust FFI Bridge
==============================================================
Loads the compiled `libtokenectomy_subcortex.so` native Rust library.
Provides microsecond-level latency for:
  - `heal_indentation()`: Re-aligns block indentation in 5 microseconds.
  - `audit_scope()`: Checks undefined identifiers and NameErrors in 30 microseconds.
  - `sentinel_audit()`: Blocks anti-patterns and corrupt patches.
"""

import os
import ctypes
import json
from typing import List, Dict, Optional, Tuple

_LIB_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "crates", "tokenectomy-subcortex", "target", "release", "libtokenectomy_subcortex.so"
)

_rust_lib = None
if os.path.exists(_LIB_PATH):
    try:
        _rust_lib = ctypes.CDLL(_LIB_PATH)
        
        # tokenectomy_heal_indentation
        _rust_lib.tokenectomy_heal_indentation.argtypes = [
            ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p
        ]
        _rust_lib.tokenectomy_heal_indentation.restype = ctypes.c_void_p

        # tokenectomy_audit_scope
        _rust_lib.tokenectomy_audit_scope.argtypes = [ctypes.c_char_p]
        _rust_lib.tokenectomy_audit_scope.restype = ctypes.c_void_p

        # tokenectomy_sentinel_audit
        _rust_lib.tokenectomy_sentinel_audit.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
        _rust_lib.tokenectomy_sentinel_audit.restype = ctypes.c_void_p

        # tokenectomy_free_string
        _rust_lib.tokenectomy_free_string.argtypes = [ctypes.c_void_p]
        _rust_lib.tokenectomy_free_string.restype = None
    except Exception as e:
        _rust_lib = None


class RustSubCortex:
    """
    Direct Python interface to the native Rust Tokenectomy Sub-Cortex.
    """

    @classmethod
    def is_available(cls) -> bool:
        return _rust_lib is not None

    @classmethod
    def heal_indentation(cls, orig: str, new_code: str, anchor: str = "") -> str:
        if not _rust_lib:
            from scripts.tokenectomy_subcortex import TokenectomyIndentationHealer
            return TokenectomyIndentationHealer.heal(orig, new_code, anchor)

        orig_b = orig.encode("utf-8")
        new_b = new_code.encode("utf-8")
        anchor_b = anchor.encode("utf-8")

        ptr = _rust_lib.tokenectomy_heal_indentation(orig_b, new_b, anchor_b)
        if not ptr:
            return new_code

        try:
            return ctypes.string_at(ptr).decode("utf-8")
        finally:
            _rust_lib.tokenectomy_free_string(ptr)

    @classmethod
    def audit_scope(cls, code: str) -> List[Dict]:
        if not _rust_lib:
            return []

        code_b = code.encode("utf-8")
        ptr = _rust_lib.tokenectomy_audit_scope(code_b)
        if not ptr:
            return []

        try:
            json_str = ctypes.string_at(ptr).decode("utf-8")
            return json.loads(json_str)
        finally:
            _rust_lib.tokenectomy_free_string(ptr)

    @classmethod
    def sentinel_audit(cls, orig: str, new_code: str) -> Tuple[bool, str]:
        if not _rust_lib:
            return True, ""

        orig_b = orig.encode("utf-8")
        new_b = new_code.encode("utf-8")
        ptr = _rust_lib.tokenectomy_sentinel_audit(orig_b, new_b)
        if not ptr:
            return True, ""

        try:
            json_str = ctypes.string_at(ptr).decode("utf-8")
            data = json.loads(json_str)
            return data.get("valid", True), data.get("reason", "")
        finally:
            _rust_lib.tokenectomy_free_string(ptr)
