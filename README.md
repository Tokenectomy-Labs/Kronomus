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

## 📊 Empirical Benchmark Results (SWE-bench Verified)

Read the official full 500-instance benchmark report in [BENCHMARK_500_REPORT.md](BENCHMARK_500_REPORT.md).

<p align="center">
  <img src="assets/benchmark_run1_vs_run2.svg" alt="Kronumos Runner 1 vs Runner 2 Progression" width="760" />
</p>

* **Evaluated Tasks**: 500 / 500 (100% completed, 0 OOM crashes)
* **Officially Resolved Tasks (`Pass@1`)**: **10 Resolved** (12.66% resolution rate on candidate patches)
* **Verified Ecosystems**: Solved production issues in **Django (5), Scikit-Learn (2), Pytest (1), PyData Xarray (1), and SymPy (1)**
* **GNU Patch Validity**: 100.0% clean application rate (*0 patch apply errors, 0 Docker crashes*)
* **Average Turns to Remediation**: 1.97 turns
* **Average Token Consumption**: 3,009 tokens / task (*98.2% token bloat reduction*)
* **Average Remediation Latency**: 43.6 seconds / task
* **Marginal Inference Cost**: **$0.00 (Self-Hosted / Cloudflare Edge)**

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

## 💻 Interactive CLI Agent (Transparent Terminal REPL)

Kronumos includes a native agentic CLI interface featuring an ambient, transparent-terminal aesthetic, live streaming tokens, and an autonomous repair loop:

```text
  ╦╔═╦═╗╔═╗╔╗╔╦ ╦╔╦╗╔═╗╔═╗
  ╠╩╗╠╦╝║ ║║║║║ ║║║║║ ║╚═╗
  ╩ ╩╩╚═╚═╝╝╚╝╚═╝╩ ╩╚═╝╚═╝
  Autonomous Code Remediation & SRE Agent • v1.0

╭──────────────────────────────────────────────────────────────╮
│  Workspace : /home/developer/payment-service                 │
│  Project   : Rust (Cargo)                                    │
│  Backend   : cloudflare                                      │
│  Sub-Cortex: ACTIVE (Zero-Leak Redaction + AST)              │
╰──────────────────────────────────────────────────────────────╯

Interactive Agent Commands:
  Any text     chat with Kronumos or explain code/errors
  /fix         autonomous diagnostics & repair loop
  /diff        inspect git diff in workspace
  /test        run test suite with Sub-Cortex scrubbing
  /clear       clear conversation memory buffer
  /help        display help and shortcuts
  /exit        exit Kronumos cleanly

⚡ kronumos ❯ 
```

### Installation

```bash
# Via Cargo:
cargo install --git https://github.com/Tokenectomy-Labs/Tokenectomy --bin kronumos

# Or 1-line installer:
curl -fsSL https://raw.githubusercontent.com/Tokenectomy-Labs/Kronomus/main/cli/install.sh | bash
```

### Usage

```bash
# 1. Interactive terminal chat REPL:
kronumos

# 2. Autonomous test-driven repair loop:
kronumos --fix

# 3. Choose your backend (Cloudflare Edge, Local Ollama, or OpenAI/Groq):
kronumos --backend cloudflare --cf-url https://kronumos-gateway.<account>.workers.dev
kronumos --backend ollama --ollama-model hf.co/NadevA23/Kronumos-GGUF:Q4_K_M
```

---

## ☁️ Zero-Cost Cloudflare Edge Gateway ($0 Serverless)

Deploy Kronumos on Cloudflare's global edge network in under 60 seconds with **$0 server infrastructure cost** using Cloudflare Workers AI:

```bash
# 1. Navigate to the gateway directory:
cd gateway

# 2. Deploy directly to the edge:
npm run deploy
```

* **Free Tier Allocation**: 10,000 Neurons per day (~500+ debugging turns/day for free).
* **Global Edge Acceleration**: Runs on Cloudflare edge GPUs across 300+ datacenters worldwide.
* **Architecture Details**: See [`gateway/README.md`](gateway/README.md).

---

## 🏠 Offline Local Inference via Ollama

Run Kronumos 100% locally and offline with GGUF quantization:

```bash
ollama run hf.co/NadevA23/Kronumos-GGUF:Q4_K_M
```

---

## 🐍 Python SDK (Transformers)

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

