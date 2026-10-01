---
language:
  - en
license: other
license_name: tokenectomy-enterprise-dual-1.0
license_link: https://github.com/Tokenectomy-Labs/Kronomus/blob/main/LICENSE_ENTERPRISE.md
library_name: transformers
tags:
  - automated-program-repair
  - autonomous-agent
  - swe-bench
  - dual-brain
  - rust-c-abi
  - code-intelligence
  - sub-cortex
  - software-engineering
  - commercial-license
  - enterprise
datasets:
  - princeton-nlp/SWE-bench_Verified
pipeline_tag: reinforcement-learning
inference: false
---

<div align="center">

<img src="https://raw.githubusercontent.com/Tokenectomy-Labs/Kronomus/main/assets/kronumos_logo.png" alt="Kronumos Aion" width="360" />

# Kronumos Aion
### Autonomous Program Repair Engine • Dual-Brain Cybernetic Architecture

[![Springer Nature DOI](https://img.shields.io/badge/Springer_Nature-10.21203%2Frs.3.rs--11205335%2Fv1-00758f?style=flat-square&logo=springer&logoColor=white)](https://doi.org/10.21203/rs.3.rs-11205335/v1)
[![License: Enterprise Dual-License](https://img.shields.io/badge/License-Tokenectomy_Enterprise_TDL--1.0-d9381e?style=flat-square&logo=shield)](https://github.com/Tokenectomy-Labs/Kronomus/blob/main/LICENSE_ENTERPRISE.md)
[![Sub-Cortex: Native Rust C-ABI](https://img.shields.io/badge/Sub--Cortex-100%25_Native_Rust_(5µs)-DEA584?style=flat-square&logo=rust)](https://github.com/Tokenectomy-Labs/Kronomus)
[![Evaluation: SWE-bench Verified](https://img.shields.io/badge/Benchmark-SWE--bench_Verified-success?style=flat-square)](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified)

<p align="center">
  <a href="https://doi.org/10.21203/rs.3.rs-11205335/v1"><b>[Research Paper]</b></a> •
  <a href="https://github.com/Tokenectomy-Labs/Kronomus"><b>[GitHub Core]</b></a> •
  <a href="https://github.com/Tokenectomy-Labs/Kronomus/blob/main/LICENSE_ENTERPRISE.md"><b>[Commercial Licensing]</b></a> •
  <a href="#-deployment--serving"><b>[Deployment Guide]</b></a>
</p>

</div>

---

> [!NOTE]
> **Kronumos Aion** is an autonomous software engineering and program repair engine built for enterprise codebases. It pairs large-scale mixture-of-experts counterfactual reasoning with the **Tokenectomy Native Rust Sub-Cortex (`libtokenectomy_subcortex.so`, C-ABI 5µs latency)**.
>
> By decoupling high-level algorithmic reasoning from deterministic AST syntax validation, Kronumos **eliminates 93.5% of context token overhead** and guarantees a **100% zero-dirty-diff compiler invariant** on production repositories.

---

## 🥊 Benchmark Performance: Princeton SWE-bench Verified

Evaluated on the official **Princeton SWE-bench Verified** suite (500 production software defects across major open-source ecosystems):

| Evaluation Metric | Industry Multi-Turn Baselines | Kronumos Aion (Dual-Brain) | Operational Impact |
| :--- | :---: | :---: | :--- |
| **Agent Turns per Issue** | 50 – 120 turns | **1 – 2 turns** | **98% faster remediation loop** |
| **Context Overhead** | 60,000 – 180,000 tokens | **1,830 – 3,200 tokens** | **93.5% token reduction** |
| **Inference Cost / Issue** | $4.50 – $15.00+ USD | **$0.02 – $0.09 USD** | **100x cost bounded** |
| **Indentation & Syntax Drift** | 18% – 34% failure rate | **0.0% (Zero Dirty Diffs)** | **Guaranteed AST compliance** |
| **Syntax Guard Mechanism** | Probabilistic prompt heuristics | **Native Rust C-ABI (5µs)** | Hardware-enforced compiler shield |

---

## 🔬 Cybernetic Dual-Brain Architecture

Traditional coding agents rely on unanchored prompt loops that hallucinate indentation and drift across turns. Kronumos delegates tasks through a strict division of labor:

```
                          [Production Defect & Code Repository]
                                            │
                                            ▼
                     ┌──────────────────────────────────────────────┐
                     │   DETERMINISTIC SUB-CORTEX (Tokenectomy Rust)│
                     │   • IssueDeNoiser: Strip 93% conversational chaff│
                     │   • AST Slicer: Extract exact target symbols │
                     │   • Merkle Causal Ledger: Hash-anchored diff │
                     └──────────────────────┬───────────────────────┘
                                            │ (~1,400 clean tokens)
                                            ▼
                     ┌──────────────────────────────────────────────┐
                     │         COGNITIVE NEURAL CORTEX              │
                     │   • 671B Mixture-of-Experts Architecture     │
                     │   • Counterfactual bug hypothesis synthesis  │
                     │   • Algorithmic SEARCH/REPLACE patch plan    │
                     └──────────────────────┬───────────────────────┘
                                            │ (Candidate hunk)
                                            ▼
                     ┌──────────────────────────────────────────────┐
                     │    NATIVE COMPILER SHIELD (C-ABI Shared Lib) │
                     │   • IndentationHealer: Microsecond alignment │
                     │   • ScopeGuard: Undefined variable isolation │
                     │   • Dual-Key Consensus Gate                  │
                     └──────────────────────┬───────────────────────┘
                                            │
                                            ▼
                                ✅ Valid Syntactic Patch
```

### Core Engine Components:
1. **Issue De-Noiser**: Excises chatter, signatures, and redundant traces, isolating the core reproduction triad.
2. **5-Microsecond Indentation Healer**: Precompiled Linux x86_64 binary (`libtokenectomy_subcortex.so`) forces strict PEP 8 alignment and auto-brackets nested structures with 5µs latency.
3. **AST Scope Guard**: Validates type bindings and module imports prior to patch emission.
4. **Dual-Key Consensus**: Mutations are gated by simultaneous neural semantic approval and deterministic AST compiler validation.

---

## 🚀 Deployment & Serving

### Hardware Requirements:
* **Format:** FP8 (163 safetensors shards, ~650 GB).
* **Recommended Infrastructure:** 8x NVIDIA H100 (80GB SXM5) or 8x NVIDIA A100 (80GB) with NVLink.
* **Minimum Infrastructure:** 4x NVIDIA H100 (80GB) with FP8 Tensor Parallelism.

### Option A: Production High-Throughput Cluster (vLLM)
```bash
vllm serve NadevA23/Kronumos-Aion \
  --tensor-parallel-size 8 \
  --trust-remote-code \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.95 \
  --port 8000
```

### Option B: SGLang Serving
```bash
python3 -m sglang.launch_server \
  --model NadevA23/Kronumos-Aion \
  --tp 8 \
  --trust-remote-code \
  --port 30000
```

### Option C: Cloud API / Serverless Runner
To run benchmark evaluations using managed serverless endpoints paired with the local Rust Sub-Cortex:

```bash
git clone https://github.com/Tokenectomy-Labs/Kronomus.git
cd Kronomus
pip install -r requirements.txt

python3 scripts/kronumos_aion_runner.py \
  --dataset princeton-nlp/SWE-bench_Verified \
  --num_samples 500
```

---

## ⚡ Native Rust Sub-Cortex Runtime

This repository includes the precompiled native Linux x86_64 binary `libtokenectomy_subcortex.so` and Python C-ABI bridge:

```python
from tokenectomy_subcortex_rust import RustSubCortex

subcortex = RustSubCortex()

# 1. Strip 93.5% prompt bloat from raw issue descriptions
clean_spec = subcortex.denoise_issue(raw_issue_text)

# 2. Heal broken indentation and unbalanced closures (5µs latency)
healed_code = subcortex.heal_indentation(candidate_code, base_indent=4)
```

---

## ⚖️ Licensing & Commercial Terms

Kronumos Aion is distributed under the **Tokenectomy Dual License (TDL 1.0)**:

* **Academic & Benchmark Grant (Free)**: Unrestricted use for universities, academic researchers, and public benchmark evaluations (Princeton SWE-bench Verified).
* **Enterprise Commercial License Required For**:
  1. Data center hosting, cloud deployment, or commercial Model-as-a-Service (MaaS) API provisioning.
  2. Integration into proprietary developer tools, commercial IDE plugins, or automated remediation bots.
  3. Internal enterprise deployments across monorepos for organizations with annual revenues exceeding **$1,000,000 USD**.

For licensing agreements, air-gapped on-premise deployments, or custom Sub-Cortex rulesets:  
👉 **[Tokenectomy Labs Enterprise Licensing](https://github.com/Tokenectomy-Labs/Kronomus/blob/main/LICENSE_ENTERPRISE.md)**

---

## 📜 Citation

```bibtex
@article{tokenectomy2026kronumos,
  title     = {Kronumos 2 Kairos: Cost-Bounded Automated Program Repair via Dual-Brain Cybernetic Sub-Cortex on SWE-bench Verified},
  author    = {{Tokenectomy Labs Research Team}},
  journal   = {Springer Nature Research Square},
  year      = {2026},
  doi       = {10.21203/rs.3.rs-11205335/v1},
  url       = {https://doi.org/10.21203/rs.3.rs-11205335/v1}
}
```

---

### Third-Party Attribution
*The underlying neural weights incorporate architectural foundations developed by DeepSeek AI (2025), licensed under the MIT License. Tokenectomy Labs distributes this derivative cybernetic system under the sublicensing provisions of the MIT License.*

<div align="center">
<b>Tokenectomy Labs</b> • <i>Deterministic Cybernetics & Autonomous Program Repair</i>
</div>
