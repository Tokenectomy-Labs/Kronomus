<p align="center">
  <img src="assets/kronumos_logo.png" alt="Kronumos - Autonomous Software Repair Agent" width="380" />
</p>

<p align="center">
  <strong><em>"You write the features. Kronumos heals the bugs."</em></strong>
</p>

<p align="center">
  <a href="https://doi.org/10.5281/zenodo.22929676"><img src="https://zenodo.org/badge/DOI/10.5281/zenodo.22929676.svg" alt="DOI: 10.5281/zenodo.22929676" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-AGPLv3_%2F_Commercial-blue.svg" alt="License: AGPLv3 / Commercial" /></a>
  <a href="https://huggingface.co/NadevA23/Kronumos"><img src="https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NadevA23%2FKronumos-yellow" alt="Hugging Face Model" /></a>
  <a href="https://huggingface.co/NadevA23/Kronumos-GGUF"><img src="https://img.shields.io/badge/GGUF-Quantized-green" alt="GGUF Quantized" /></a>
</p>


## 📌 What is Kronumos?

**Kronumos** is a specialized autonomous software engineering agent, fine-tuned specifically for end-to-end bug remediation and automated self-healing — not generic chatbot coding.

Generic AI coding assistants try to do everything: generating unverified applications, hallucinating missing functions, and bloating context with massive raw runtime logs.

Kronumos is scoped narrower and deeper. It handles a single, closed-loop engineering workflow:
1. **Diagnose** runtime failures & test crashes from raw error logs.
2. **Sub-Cortex Token Surgery**: Excise framework noise and redact sensitive credentials (JWT, AWS, DB keys) using Tokenectomy Rust engine (91.3% token reduction).
3. **Analyze Blast Radius**: Map caller dependency graphs before applying edits.
4. **Synthesize & Verify Atomic Patch**: Apply search-and-replace AST patches with zero dirty diffs.
5. **Git Delivery**: Automatically branch, commit, open Pull Requests, and close incident tracking issues.


## 📄 Academic Paper & Preprint

Read the formal preprint paper on Zenodo: **[DOI: 10.5281/zenodo.22929676](https://doi.org/10.5281/zenodo.22929676)**, read the [Technical Report](paper/KRONUMOS_TECHNICAL_REPORT.md), or view the publication-ready LaTeX source in [paper/main.tex](paper/main.tex):

> **"Kronumos: Cost-Bounded Automated Program Repair via Context Surgery and POSIX Diff Re-Anchoring on SWE-bench Verified"**  
> *Author: Tokenectomy Labs*  
> *Permanent DOI: [10.5281/zenodo.22929676](https://doi.org/10.5281/zenodo.22929676)*


## 🗺️ Product & Engineering Roadmap

Read the complete engineering roadmap and evaluation methodology in [kronumos_product.roadmap.md](kronumos_product.roadmap.md).


## 📊 Empirical Benchmark Results (SWE-bench Verified)

Read the official full 500-instance benchmark report in [BENCHMARK_500_REPORT.md](BENCHMARK_500_REPORT.md).

<p align="center">
  <img src="assets/figure1_swebench_ablation.svg" alt="Figure 1: Empirical ablation of the Tokenectomy Sub-Cortex on SWE-bench Verified (N = 500)" width="800" />
</p>

* **Evaluated Tasks**: 500 / 500 tasks (475 synthesized, 25 structural safe refusals)
* **Officially Resolved Tasks (`Pass@1`)**: **12 Resolved** (15.0% candidate precision on Docker-evaluated tasks, 2.4% full-benchmark lower bound [1.4%, 4.1%])
* **Verified Ecosystems**: Solved production issues in **Django (7), Scikit-Learn (2), Pytest (1), PyData Xarray (1), and SymPy (1)**
* **GNU Patch Validity**: 100.0% clean application rate (*0 hunk errors on evaluated instances*)
* **Average Turns to Remediation**: 2.34 turns
* **Average Token Consumption**: 3,361.0 tokens / task (*91.3% token bloat reduction vs raw context*)
* **Average Remediation Latency**: 43.6 seconds / task
* **Marginal Inference Cost**: **$0.00 (Self-Hosted / Cloudflare Edge)**


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


## 💻 Interactive CLI Agent (Transparent Terminal REPL)

Kronumos includes a native agentic CLI interface featuring an ambient, transparent-terminal aesthetic, live streaming tokens, and an autonomous repair loop:

```text
    ██╗  ██╗██████╗  ██████╗ ███╗   ██╗██╗   ██╗███╗   ███╗ ██████╗ ███████╗
    ██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██║   ██║████╗ ████║██╔═══██╗██╔════╝
    █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║   ██║██╔████╔██║██║   ██║███████╗
    ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██║╚██╔╝██║██║   ██║╚════██║
    ██║  ██╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝███████║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚══════╝

                     · K R O N U M O S   K A I R O S ·
               Autonomous Code Remediation & SRE Agent • v1.0

Interactive Agent Commands:
  Any text     chat with Kronumos or explain code/errors
  /fix         autonomous diagnostics & repair loop
  /diff        inspect git diff in workspace
  /test        run test suite on physical hardware
  /doctor      run diagnostic environment & gateway health check
  /stats       display FinOps token savings & telemetry
  /undo        revert uncommitted patches (zero dirty diff)
  /clear       clear conversation memory buffer
  /help        display help and shortcuts
  /exit        exit Kronumos cleanly

⚡ kronumos ❯ 
```

### Installation

```bash
# 1-Line Cryptographic Installer (Linux x86_64, with automated SHA256 verification):
curl -fsSL https://raw.githubusercontent.com/Tokenectomy-Labs/Kronomus/main/cli/install.sh | bash

# Or download pre-compiled standalone release binaries directly:
# https://github.com/Tokenectomy-Labs/Kronomus/releases/latest
```

### Usage Modes

```bash
# 1. Autonomous TDD self-healing loop (runs test suite, patches, verifies on hardware):
kronumos --fix
kronumos --fix -t "pytest tests/test_auth.py"  # Custom test command override
kronumos --fix --auto-rollback                  # Auto-revert broken patches on failure (0 dirty diff)
kronumos --fix --branch fix/auth --commit      # Auto Git branch & commit on pass
kronumos --fix --pr                            # End-to-end Git delivery: auto-branch, commit, & open Pull Request
kronumos --fix --json                          # Machine-to-machine JSON output for CI/CD

# 2. Diagnostic environment & edge connectivity check:
kronumos --doctor
kronumos --doctor --json                       # Structured diagnostic output for CI/CD

# 3. One-shot terminal command execution (headless):
kronumos "Explain the blast radius of refactoring auth module"

# 4. Unix piping (clean quiet mode for CI/CD or log diagnosis):
cat error.log | kronumos -q
pytest 2>&1 | kronumos -q "Diagnose and fix assertions"

# 5. Interactive ambient terminal REPL:
kronumos

# 6. Multi-Backend inference (Cloudflare Edge, Local Ollama, OpenAI/Groq):
kronumos --backend cloudflare                 # Hosted edge gateway (zero-config, free tier)
kronumos --backend ollama --ollama-model hf.co/NadevA23/Kronumos-GGUF:Q4_K_M
kronumos --backend openai --openai-key $GROQ_API_KEY --openai-model llama-3.3-70b-versatile
```


### GitHub Actions CI/CD Integration

Automate bug remediation directly inside your repository pipelines with the official GitHub Action:

```yaml
name: "Autonomous Remediation"
on: [pull_request, workflow_dispatch]

jobs:
  self-heal:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Auto-Remediate Test Failures
        uses: Tokenectomy-Labs/Kronomus@main
        with:
          test-cmd: "pytest tests/"
          auto-rollback: "true"
          commit: "true"
```


## 🧪 Live Bug Arenas & Reproducible Benchmarks

Explore standalone, authentic bug arenas designed to test autonomous repair agents on physical hardware without mocks or simulations:

* **[Linux Kernel Circular Buffer (`kfifo`) Boundary Defect](examples/linux-kfifo-bug)**:
  Authentic off-by-one boundary defect (`>` vs `>=`) causing ring buffer silent byte corruption. Resolved by Kronumos in 18 seconds (round 4).
* **[CVE Memory Lifecycle Defect (AddressSanitizer Heap-Use-After-Free)](examples/cve-memory-lifecycle-bug)**:
  Authentic systems security bug under GCC `-fsanitize=address -fsanitize=undefined` modeled after network daemon CVE patterns (Redis/libcurl). Naive LLMs trigger LeakSanitizer aborts; Kronumos synthesizes a surgical memory-safe patch in round 1.



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


## 🏠 Offline Local Inference via Ollama

Run Kronumos 100% locally and offline with GGUF quantization:

```bash
ollama run hf.co/NadevA23/Kronumos-GGUF:Q4_K_M
```


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


## 🏢 Organization & Compliance
- **Engineering & Maintenance:** Tokenectomy Labs
- **License:** Dual License (GNU Affero General Public License v3 / Commercial Enterprise) — see [`LICENSE`](LICENSE)
- **Terms of Service:** [`TERMS.md`](TERMS.md)
- **Privacy & Zero-Retention Policy:** [`PRIVACY.md`](PRIVACY.md)
- **Security Policy:** [`SECURITY.md`](SECURITY.md)


## 📖 Citation

If you use Kronumos in your research or benchmarks, please cite our preprint:

```bibtex
@article{tokenectomy2026kronumos,
  author    = {Tokenectomy Labs},
  title     = {Kronumos: Cost-Bounded Automated Program Repair via Context Surgery and POSIX Diff Re-Anchoring on SWE-bench Verified},
  journal   = {Zenodo},
  year      = {2026},
  month     = sep,
  doi       = {10.5281/zenodo.22929676},
  url       = {https://doi.org/10.5281/zenodo.22929676}
}
```

