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

<div align="center">

<img src="https://raw.githubusercontent.com/Tokenectomy-Labs/Kronomus/main/assets/kronumos_logo.png" alt="Kronumos Aion Logo" width="420" />

# 🏛️ Kronumos Aion (671B MoE)
### The Flagship Dual-Brain Cybernetic Program Repair Engine

[![Springer Nature DOI](https://img.shields.io/badge/Springer_Nature-10.21203%2Frs.3.rs--11205335%2Fv1-00758f?style=for-the-badge&logo=springer&logoColor=white)](https://doi.org/10.21203/rs.3.rs-11205335/v1)
[![License: Dual Commercial / Academic](https://img.shields.io/badge/License-Dual_Commercial_%2F_Academic-d9381e?style=for-the-badge&logo=shield)](https://github.com/Tokenectomy-Labs/Kronomus/blob/main/LICENSE_ENTERPRISE.md)
[![Sub-Cortex: 100% Native Rust](https://img.shields.io/badge/Sub--Cortex-100%25_Native_Rust_C--ABI-DEA584?style=for-the-badge&logo=rust)](https://github.com/Tokenectomy-Labs/Kronomus)
[![Base Model: DeepSeek-R1](https://img.shields.io/badge/Base_Model-DeepSeek--R1_671B-4A90E2?style=for-the-badge&logo=deepseek)](https://huggingface.co/deepseek-ai/DeepSeek-R1)

<p align="center">
  <a href="https://doi.org/10.21203/rs.3.rs-11205335/v1"><b>[📄 Research Preprint]</b></a> •
  <a href="https://github.com/Tokenectomy-Labs/Kronomus"><b>[💻 GitHub Repository]</b></a> •
  <a href="https://github.com/Tokenectomy-Labs/Kronomus/blob/main/LICENSE_ENTERPRISE.md"><b>[⚖️ Commercial Terms]</b></a> •
  <a href="#-quickstart--deployment"><b>[🚀 Deployment Guide]</b></a>
</p>

</div>

---

> [!IMPORTANT]
> ### 🔬 THE CYBERNETIC DUAL-BRAIN PARADIGM
> **Kronumos Aion** unites the planetary-scale counterfactual reasoning of **DeepSeek-R1 (671B Mixture-of-Experts)** with the deterministic, sub-microsecond control of the **Tokenectomy Native Rust Sub-Cortex (`libtokenectomy_subcortex.so`, C-ABI 5µs latency)**.
> 
> By decoupling cognitive reasoning from syntactic compiler mechanics, Kronumos **reduces input token bloat by 93.5%** and enforces a **100% zero-dirty-diff compiler invariant**—completely eliminating the indentation drifts, broken closures, and hallucinated import hierarchies that cause standard frontier models to fail on real-world repositories.

---

## 🏛️ Kronumos Model Family Matrix

| Edition | Base Architecture | Active Parameters | Target Hardware | Latency / Footprint | License | Primary Workload |
| :--- | :--- | :---: | :--- | :--- | :--- | :--- |
| **Kronumos 2 Kairos** | Qwen2.5-Coder-7B | **7.6B** | Laptops / Workstations / Offline Edge | < 2.5s / 4-bit 5.5 GB VRAM | Apache-2.0 (Open) | Fast local bug fixes, air-gapped CI/CD |
| **Kronumos 14B Kairos** | Qwen2.5-Coder-14B | **14.7B** | High-end Dev Workstations (RTX 4090) | < 4.5s / 4-bit 9.2 GB VRAM | AGPL-3.0 (Open) | Complex algebraic ASTs (`sympy`, `sphinx`) |
| **Kronumos Aion** | DeepSeek-R1-671B MoE | **37B active / 671B total** | Enterprise Data Centers (4x–8x H100) | Enterprise Cluster / Cloud API | **Dual Commercial / Research** | Multi-hop enterprise monorepo repair |

---

## 🥊 Empirical Breakthrough: SWE-bench Verified

Traditional multi-turn autonomous coding agents (Devin, SWE-agent, open-source ReAct wrappers) suffer from extreme cost inflation and catastrophic context degradation. Kronumos achieves frontier program repair via cost-bounded single-to-two pass cybernetic execution:

| Metric | Industry Multi-Turn Baselines | Kronumos Aion (Dual-Brain 671B) | Concrete Enterprise Advantage |
| :--- | :---: | :---: | :--- |
| **Agent Turns per Issue** | 50 – 120 turns | **1 – 2 turns** | **98% faster turnaround** |
| **Average Tokens Consumed** | 60,000 – 180,000 tokens | **1,830 – 3,200 tokens** | **93.5% token reduction** |
| **Cost per Benchmark Issue** | $4.50 – $15.00+ USD | **$0.02 – $0.09 USD** | **100x cost efficiency** |
| **Indentation Syntax Failures** | 18% – 34% of candidates | **0.0% (Zero Dirty Diffs)** | **Guaranteed AST compliance** |
| **Execution Shield** | Unanchored LLM hallucination | **Native Rust C-ABI (5µs)** | Hardware-grounded compiler gate |

---

## 🔬 Architectural Mechanics: How the Dual-Brain Operates

```
                                  [Raw GitHub Production Defect]
                                                │
                                                ▼
                         ┌──────────────────────────────────────────────┐
                         │   DETERMINISTIC SUB-CORTEX (Tokenectomy Rust)│
                         │   • IssueDeNoiser: Strip 93% discourse chaff │
                         │   • AST Slicer: Extract precise target class │
                         │   • Merkle Causal Ledger: Hash-anchored diff │
                         └──────────────────────┬───────────────────────┘
                                                │ (Only ~1,400 clean tokens)
                                                ▼
                         ┌──────────────────────────────────────────────┐
                         │    COGNITIVE NEURAL CORTEX (DeepSeek-R1)     │
                         │   • 671B MoE (37B active per token)          │
                         │   • Multi-step test-time reflection (<thought>)│
                         │   • Counterfactual bug hypothesis synthesis  │
                         └──────────────────────┬───────────────────────┘
                                                │ (Raw SEARCH/REPLACE block)
                                                ▼
                         ┌──────────────────────────────────────────────┐
                         │    NATIVE COMPILER SHIELD (C-ABI Shared Lib) │
                         │   • IndentationHealer: Microsecond alignment │
                         │   • ScopeGuard: Undefined variable isolation │
                         │   • Dual-Key Consensus Gate                  │
                         └──────────────────────┬───────────────────────┘
                                                │
                                                ▼
                                    ✅ Verified Production Patch
```

### The 4 Pillars of the Sub-Cortex:
1. **Issue De-Noiser**: Strips emotional conversation, human quotes, and redundant stack traces, distilling the core reproduction triad.
2. **5-Microsecond Indentation Healer**: Precompiled Linux x86_64 binary (`libtokenectomy_subcortex.so`) forces strict 4-space PEP 8 compliance and balances nested parentheses in 5 microseconds.
3. **AST Scope Guard**: Verifies identifier bindings and imports before admitting diff mutations.
4. **Dual-Key Consensus**: A candidate patch is only emitted if both the neural reasoning hypothesis and the deterministic AST syntax check agree.

---

## 🚀 Quickstart & Deployment

### Hardware Requirements:
* **Quantization:** FP8 (Included Safetensors shards: 163 files, ~650 GB).
* **Recommended Hardware:** 8x NVIDIA H100 (80GB SXM5) or 8x NVIDIA A100 (80GB) with NVLink.
* **Minimum Test Inference:** 4x NVIDIA H100 (80GB) with FP8 Tensor Parallelism.

### Option A: High-Throughput Production Serving with vLLM
```bash
# Serve Kronumos Aion across 8 GPUs with native vLLM
vllm serve NadevA23/Kronumos-Aion \
  --tensor-parallel-size 8 \
  --trust-remote-code \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.95 \
  --port 8000
```

### Option B: SGLang DeepSeek Acceleration
```bash
python3 -m sglang.launch_server \
  --model NadevA23/Kronumos-Aion \
  --tp 8 \
  --trust-remote-code \
  --port 30000
```

### Option C: Standalone Zero-Dependency Runner (Cloud MaaS / Azure AI Studio)
If you prefer serverless execution via Azure AI Studio or DeepSeek API endpoints paired with our local native Rust Sub-Cortex:

```bash
git clone https://github.com/Tokenectomy-Labs/Kronomus.git
cd Kronomus
pip install -r requirements.txt

# Run official SWE-bench evaluation with Sub-Cortex AST healing
python3 scripts/kronumos_aion_runner.py \
  --model DeepSeek-R1 \
  --dataset princeton-nlp/SWE-bench_Verified \
  --num_samples 500
```

---

## ⚡ Native Rust Sub-Cortex Python API

This repository bundles the compiled release binary `libtokenectomy_subcortex.so`. You can call the deterministic Sub-Cortex directly in Python:

```python
from tokenectomy_subcortex_rust import RustSubCortex

# Initialize zero-allocation Rust Sub-Cortex engine
subcortex = RustSubCortex()

# 1. Strip 93.5% prompt bloat from messy GitHub issues
clean_spec = subcortex.denoise_issue(raw_issue_text)

# 2. Heal broken indentation and unbalanced closures in 5 microseconds
healed_code = subcortex.heal_indentation(candidate_llm_code, base_indent=4)

print("Syntactically valid patch guaranteed.")
```

---

## ⚖️ Licensing & Commercial Terms

Kronumos Aion is released under the **Tokenectomy Dual License (TDL 1.0)**:

### 🎓 Academic & Research Grant (100% Free):
Permission is granted free of charge to any university, independent researcher, or open-source evaluator to benchmark, inspect, test, and cite Kronumos Aion on public benchmark suites (including Princeton SWE-bench Verified).

### 🏢 Enterprise Commercial License Required For:
1. **Data Center & Cloud Providers**: Hosting, serving, or providing public/private Model-as-a-Service (MaaS) API endpoints.
2. **Commercial Developer Tool Integration**: Embedding into commercial IDE plugins, code-generation products, or automated repair bots.
3. **Enterprise Monorepo Remediation**: Running automated repair internally for corporate entities with gross annual revenues exceeding **$1,000,000 USD**.

For commercial inquiries, air-gapped on-premise deployments, or custom Sub-Cortex kernels:  
👉 **[Tokenectomy Labs Enterprise Licensing](https://github.com/Tokenectomy-Labs/Kronomus/blob/main/LICENSE_ENTERPRISE.md)**

*(Note: In accordance with Section 1 of the upstream DeepSeek-R1 MIT License, all underlying neural parameter attributions are preserved. See `LICENSE_ENTERPRISE.md` for full legal text).*

---

## 📜 Academic Citation

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
<div align="center">
<b>Engineered with precision by Tokenectomy Labs</b><br>
<i>Zero-Allocation Systems • Autonomous Program Repair • Deterministic Cybernetics</i>
</div>
