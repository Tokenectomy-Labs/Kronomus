<p align="center">
  <img src="assets/kronumos_logo.png" alt="Kronumos - Autonomous Software Repair Agent" width="380" />
</p>

<p align="center">
  <strong><em>"You write the features. Kronumos heals the bugs."</em></strong>
</p>

<p align="center">
  <a href="https://opensource.org/licenses/Apache-2.0"><img src="https://img.shields.io/badge/License-Apache_2.0-blue.svg" alt="License: Apache 2.0" /></a>
  <a href="https://huggingface.co/NadevA23/Kronumos"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NadevA23%2FKronumos-yellow" alt="Hugging Face Model" /></a>
  <a href="https://huggingface.co/NadevA23/Kronumos-GGUF"><img src="https://img.shields.io/badge/GGUF-Quantized-green" alt="GGUF Quantized" /></a>
</p>

---

## 📌 What is Kronumos?

**Kronumos** is a specialized autonomous software engineering agent, fine-tuned specifically for end-to-end bug remediation and automated self-healing — not generic chatbot coding.

Generic AI coding assistants try to do everything: generating unverified applications, hallucinating missing functions, and bloating context with massive raw runtime logs.

Kronumos is scoped narrower and deeper. It handles a single, closed-loop engineering workflow:
1. **Diagnose** runtime failures & test crashes from raw error logs.
2. **Sub-Cortex Token Surgery**: Excise framework noise and redact sensitive credentials (JWT, AWS, DB keys) using Tokenectomy Rust engine (95.2% token reduction).
3. **Analyze Blast Radius**: Map caller dependency graphs before applying edits.
4. **Synthesize & Verify Atomic Patch**: Apply search-and-replace AST patches with zero dirty diffs.
5. **Git Delivery**: Automatically branch, commit, open Pull Requests, and close incident tracking issues.

---

## 🗺️ Product & Engineering Roadmap

Read the complete engineering roadmap and evaluation methodology in [kronumos_product.roadmap.md](kronumos_product.roadmap.md).

---

## 🛠️ Tool Schema (Agent Sub-Cortex)

Kronumos is fine-tuned to emit structured JSON tool calls:

| Tool | Purpose |
| :--- | :--- |
| `get_error_context` | Excise framework noise, redact credentials, and extract exact offending code snippets from raw logs |
| `apply_code_patch` | Apply an atomic search-and-replace AST patch, verified before commit |
| `inspect_docker` | Diagnose container crashes (e.g. exit code 137 OOMKilled) via logs and resource stats |
| `probe_database` | Triage connection pool starvation and lock deadlocks |
| `sentinel_analyze_blast_radius` | Map caller dependency graph for a symbol/file before applying a patch |
| `create_fix_branch` | Create a new isolated git branch for the fix |
| `commit_fix` | Commit the verified patch to the fix branch |
| `open_pull_request` | Open a PR from the fix branch to the target branch |
| `create_incident_issue` | Open a tracking issue for a diagnosed incident |
| `link_issue_to_fix_pr` | Link an existing incident issue to its resolving PR |
| `close_incident_issue` | Close the incident issue once verified and merged |

---

## 🚀 Quickstart

### Running locally via Ollama:
```bash
ollama run hf.co/NadevA23/Kronumos-GGUF:Q4_K_M
```

### Python (Transformers):
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "NadevA23/Kronumos"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
```

---

## 🏢 Organization & Author
- **Developed by:** Daffa ([@daffa2555](https://github.com/daffa2555))
- **Organization:** Tokenectomy Labs
- **License:** Apache 2.0
