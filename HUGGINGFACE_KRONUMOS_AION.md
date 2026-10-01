---
language:
- en
license: mit
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
datasets:
- princeton-nlp/SWE-bench_Verified
---

# 🏛️ Kronumos Aion — Flagship Dual-Brain Cybernetic Program Repair Engine

[![Springer Nature DOI](https://img.shields.io/badge/Springer_Nature-10.21203%2Frs.3.rs--11205335%2Fv1-00758f?style=flat-square&logo=springer&logoColor=white)](https://doi.org/10.21203/rs.3.rs-11205335/v1)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--7909--4916-A6CE39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0000-7909-4916)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Engine: 100% Native Rust C-ABI](https://img.shields.io/badge/Engine-100%25_Native_Rust_C--ABI-DEA584?style=flat-square&logo=rust)](https://github.com/Tokenectomy-Labs/Kronomus)

**Kronumos Aion** is the flagship enterprise-scale edition of the Kronumos automated program repair (APR) ecosystem. It unites the deep test-time counterfactual reasoning of **DeepSeek-R1 (671B MoE)** with the sub-millisecond deterministic control of the **Tokenectomy Native Rust Sub-Cortex (C-ABI 5µs)**.

Where lightweight models operate on agile edge workloads (**Kronumos Kairos**), **Kronumos Aion** is engineered for the deep cosmic scale of enterprise monorepos, multi-hop architectural bugs, and frontier **SWE-bench Verified** benchmark evaluations.

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
   Powered by `DeepSeek-R1` (MIT License) with thousands of test-time `<thought>` reflection tokens, evaluating multiple bug-fix hypotheses before writing code.
2. **Deterministic Token Surgery:**  
   Cuts prompt token consumption by **93.5%**, enabling frontier 671B inference at sub-dollar costs per benchmark run.
3. **5-Microsecond AST Indentation Healing:**  
   Native compiled Rust (`libtokenectomy_subcortex.so`) guarantees zero indentation drift and perfect POSIX unified diff headers.
4. **100% Permissive Commercial License:**  
   Both the base model (DeepSeek-R1) and the Sub-Cortex runtime are released under the **MIT License**, permitting unrestricted enterprise and commercial deployment.

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
@article{daffa2026kronumos,
  title={Kronumos 2 Kairos: Cost-Bounded Automated Program Repair via Dual-Brain Cybernetic Sub-Cortex on SWE-bench Verified},
  author={Daffa, Muhammad Naufal},
  journal={Springer Nature Research Square},
  year={2026},
  doi={10.21203/rs.3.rs-11205335/v1}
}
```

**ORCID Record:** [0009-0000-7909-4916](https://orcid.org/0009-0000-7909-4916)  
**Publisher:** *Springer Science and Business Media LLC*
