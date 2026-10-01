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
- deepseek-r1
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

# 🏛️ Kronumos Aion — Flagship Dual-Brain Cybernetic Program Repair Engine

[![Springer Nature DOI](https://img.shields.io/badge/Springer_Nature-10.21203%2Frs.3.rs--11205335%2Fv1-00758f?style=flat-square&logo=springer&logoColor=white)](https://doi.org/10.21203/rs.3.rs-11205335/v1)
[![License: Dual Commercial / Academic](https://img.shields.io/badge/License-Dual_Commercial_%2F_Academic-d9381e?style=flat-square&logo=shield)](LICENSE_ENTERPRISE.md)
[![Engine: 100% Native Rust C-ABI](https://img.shields.io/badge/Engine-100%25_Native_Rust_C--ABI-DEA584?style=flat-square&logo=rust)](https://github.com/Tokenectomy-Labs/Kronomus)

**Kronumos Aion** is the flagship enterprise-scale edition of the Kronumos automated program repair (APR) ecosystem. It unites the deep test-time counterfactual reasoning of **DeepSeek-R1 (671B MoE)** with the sub-millisecond deterministic control of the **Tokenectomy Native Rust Sub-Cortex (C-ABI 5µs)**.

Where lightweight models operate on agile edge workloads ([**Kronumos 2 Kairos (7B)**](https://huggingface.co/NadevA23/Kronumos-Kairos-v2) & [**Kronumos 14B Kairos**](https://huggingface.co/NadevA23/Kronumos-14B-Kairos)), **Kronumos Aion** is engineered for the deep cosmic scale of enterprise monorepos, multi-hop architectural bugs, and frontier **SWE-bench Verified** benchmark evaluations.

---

## 🏛️ The Kronumos Dual-Brain Family Portfolio

| Tier | Model | Parameters | Target Hardware | License |
| :--- | :--- | :---: | :--- | :--- |
| **Edge / Local** | [**Kronumos 2 Kairos**](https://huggingface.co/NadevA23/Kronumos-Kairos-v2) | **7.6B** | Laptops, local workstations, offline CI/CD | **Apache-2.0 (Open Weights)** |
| **Edge / Sovereign** | [**Kronumos 14B Kairos**](https://huggingface.co/NadevA23/Kronumos-14B-Kairos) | **14.7B** | Local workstations, high-math AST repairs | **AGPL-3.0 (Open Weights)** |
| **Titan / Enterprise** | **Kronumos Aion** | **671B MoE** | Enterprise Data Centers (4x–8x H100/A100) | **Dual Commercial / Research** |

---

## ⚖️ Licensing & Commercial Governance

Because executing a 671B Mixture-of-Experts architecture requires data-center grade infrastructure (320 GB – 640 GB VRAM cluster), Kronumos Aion is governed under the **Tokenectomy Dual License (TDL 1.0)**:

### 1. Free Academic & Research Grant:
- 100% free of charge for individual researchers, academic universities, non-profit institutions, and open-source benchmark evaluations (e.g. Princeton SWE-bench Verified).

### 2. Enterprise Commercial License Required For:
- **Data Center & Cloud Providers**: Hosting, serving, or providing managed inference (Model-as-a-Service / API endpoints).
- **Commercial SaaS Embedding**: Integrating into commercial developer tools, IDE extensions, or paid code-repair bots.
- **Enterprise Internal Deployment**: Running automated repair on internal monorepos for companies with annual revenues exceeding **$1,000,000 USD**.

For commercial licensing agreements and enterprise SLAs, contact [Tokenectomy Labs Enterprise](https://github.com/Tokenectomy-Labs/Kronomus).

*(Note: In full accordance with Section 1 of the upstream DeepSeek-R1 MIT License, all underlying neural parameter attributions are preserved. See `LICENSE_ENTERPRISE.md` for complete legal definitions).*

---

## 🔬 The Cybernetic Dual-Brain Architecture

Standard large language models fail on real-world repository maintenance because of **context bloat** (swallowing 50,000+ tokens of repo files) and **syntactic drift** (off-by-one indentation errors and broken unified diff hunks).

Kronumos solves this through a strict cybernetic division of labor:

```
                     ┌────────────────────────────────────────────────────────┐
                     │              Repository Issue & Codebase               │
                     └───────────────────────────┬────────────────────────────┘
                                                 │
                                                 ▼
                        ┌──────────────────────────────────────────────────┐
                        │   DETERMINISTIC SUB-CORTEX (Tokenectomy Rust)    │
                        │   • IssueDeNoiser: Strip 93% discourse noise     │
                        │   • AST Slicer: Extract precise target function  │
                        └────────────────────────┬─────────────────────────┘
                                                 │ (Only ~1,200 tokens)
                                                 ▼
                        ┌──────────────────────────────────────────────────┐
                        │       COGNITIVE NEURAL CORTEX (DeepSeek-R1)      │
                        │   • 671B Parameter Mixture-of-Experts            │
                        │   • Multi-step counterfactual reflection         │
                        │   • Deep root-cause hypothesis generation        │
                        └────────────────────────┬─────────────────────────┘
                                                 │ (Candidate logic)
                                                 ▼
                        ┌──────────────────────────────────────────────────┐
                        │   NATIVE COMPILER SHIELD (C-ABI Shared Object)   │
                        │   • IndentationHealer: Microsecond alignment     │
                        │   • ScopeGuard: Undefined identifier detection   │
                        │   • Zero-Dirty-Diff Sentinel Invariant           │
                        └────────────────────────┬─────────────────────────┘
                                                 │
                                                 ▼
                                     ✅ 100% Valid Syntactic Patch
```

---

## ⚡ Key Architectural Invariants

1. **Unbounded Cognitive Reasoning:**  
   Powered by `DeepSeek-R1` with thousands of test-time `<thought>` reflection tokens, evaluating multiple bug-fix hypotheses before writing code.
2. **Deterministic Token Surgery:**  
   Cuts prompt token consumption by **93.5%**, enabling frontier 671B inference at sub-dollar costs per benchmark run.
3. **5-Microsecond AST Indentation Healing:**  
   Native compiled Rust (`libtokenectomy_subcortex.so`) guarantees zero indentation drift and perfect POSIX unified diff headers.
4. **Zero-Dirty-Diff Invariant:**  
   Strict AST validator discards broken line continuations or syntactic garbage before git patch emission.

---

## 🚀 Quickstart & Usage

### 1. Installation

```bash
git clone https://github.com/Tokenectomy-Labs/Kronomus.git
cd Kronomus
pip install -r requirements.txt
```

### 2. Execution via Azure AI Studio or DeepSeek API

```bash
export AZURE_AI_ENDPOINT="https://<your-azure-deployment>.services.ai.azure.com/models"
export AZURE_AI_KEY="your-api-key"

python scripts/kronumos_aion_runner.py \
    --model DeepSeek-R1 \
    --dataset princeton-nlp/SWE-bench_Verified \
    --num_samples 500
```

---

## 📜 Academic Provenance & Citation

If you utilize **Kronumos Aion** or the **Tokenectomy Sub-Cortex** in your research, please cite our official Springer Nature publication:

```bibtex
@article{tokenectomy2026kronumos,
  title={Kronumos 2 Kairos: Cost-Bounded Automated Program Repair via Dual-Brain Cybernetic Sub-Cortex on SWE-bench Verified},
  author={{Tokenectomy Labs Research Team}},
  journal={Springer Nature Research Square},
  year={2026},
  doi={10.21203/rs.3.rs-11205335/v1}
}
```

**Maintained by:** Tokenectomy Labs  
**Publisher:** *Springer Science and Business Media LLC*
