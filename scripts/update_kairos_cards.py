#!/usr/bin/env python3
"""
⚡ Kronumos Hub Sync — Synchronize Model Cards & Sub-Cortex Across Repositories
=============================================================================
Updates Hugging Face model cards for the Kronumos ecosystem:
- Removes generic 'pipeline_tag: text-generation' (replaces with 'reinforcement-learning' + 'inference: false')
- Embeds verified Springer Nature DOI (10.21203/rs.3.rs-11205335/v1) and ORCID (0009-0000-7909-4916)
- Ships native libtokenectomy_subcortex.so binary and Python C-ABI bridge
- Aligns tiering: Kronumos Kairos (Edge: 7B/14B) vs Kronumos Aion (Titan: 671B MoE)
"""

import os
import sys
from huggingface_hub import HfApi

def get_token():
    with open('.env') as f:
        for line in f:
            if line.startswith('HF_TOKEN='):
                return line.strip().split('=', 1)[1]
    return os.environ.get("HF_TOKEN", "")

TOKEN = get_token()
if not TOKEN:
    print("❌ Error: HF_TOKEN not found in .env!")
    sys.exit(1)

api = HfApi(token=TOKEN)

SO_PATH = "/home/nans/web anonim/crates/tokenectomy-subcortex/target/release/libtokenectomy_subcortex.so"
BRIDGE_PATH = "/home/nans/web anonim/scripts/tokenectomy_subcortex_rust.py"

# ==========================================
# 1. NadevA23/Kronumos-Kairos-v2
# ==========================================
KAIROS_V2_README = """---
base_model: unsloth/qwen2.5-coder-7b-instruct-bnb-4bit
tags:
- reinforcement-learning
- transformers
- unsloth
- qwen2
- swe-bench
- autonomous-agents
- program-repair
- code-generation
- rust-subcortex
- dual-brain
- automated-program-repair
license: apache-2.0
language:
- en
datasets:
- princeton-nlp/SWE-bench_Verified
pipeline_tag: reinforcement-learning
inference: false
---

# ⚡ Kronumos 2 Kairos: The Dual-Brain Sub-Cortex Autonomous Program Repair Engine

[![Springer Nature DOI](https://img.shields.io/badge/Springer_Nature-10.21203%2Frs.3.rs--11205335%2Fv1-00758f?style=flat-square&logo=springer&logoColor=white)](https://doi.org/10.21203/rs.3.rs-11205335/v1)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--7909--4916-A6CE39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0000-7909-4916)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Engine: 100% Native Rust C-ABI](https://img.shields.io/badge/Engine-100%25_Native_Rust_C--ABI-DEA584?style=flat-square&logo=rust)](https://github.com/Tokenectomy-Labs/Kronomus)

**Organization:** Tokenectomy Labs  
**Base Model:** Qwen/Qwen2.5-Coder-7B-Instruct  
**Research Preprint:** Springer Nature Research Square ([DOI: 10.21203/rs.3.rs-11205335/v1](https://doi.org/10.21203/rs.3.rs-11205335/v1))  
**Lead Author:** Muhammad Naufal Daffa ([ORCID: 0009-0000-7909-4916](https://orcid.org/0009-0000-7909-4916))  
**GitHub Repository:** [Tokenectomy-Labs/Kronomus](https://github.com/Tokenectomy-Labs/Kronomus)  

**Kronumos 2 Kairos** is an open-weight 7B cybernetic autonomous program repair (APR) model fine-tuned for high-precision code remediation on real-world production software bugs. It pairs parametric neural intuition with a deterministic, zero-allocation Rust Sub-Cortex (`libtokenectomy_subcortex.so`, C-ABI 5µs latency).

---

## 🏛️ The Kronumos Dual-Brain Family Portfolio

| Tier | Model | Parameters | Target Workload | Latency / Footprint |
| :--- | :--- | :---: | :--- | :--- |
| **Edge / Workstation** | **Kronumos 2 Kairos** | **7.6B** | Rapid local bug remediation, offline laptops, CI/CD gates | **<2.5s / 4-bit 5.5 GB VRAM** |
| **Edge / Sovereign** | **Kronumos 14B Kairos** | **14.7B** | Complex algebraic, cross-module AST repairs (`sympy`, `sphinx`) | **<4.5s / 4-bit 9.2 GB VRAM** |
| **Titan / Enterprise** | [Kronumos Aion](https://huggingface.co/NadevA23/Kronumos-Aion) | **671B MoE** | Deep multi-hop counterfactual reasoning & frontier SWE-bench | **Enterprise Cluster / Cloud API** |

---

## 🥊 Benchmark Verification: SWE-bench Verified (500 Instances)

Evaluated end-to-end on the official **Princeton SWE-bench Verified** benchmark (500 production instances across Django, Scikit-Learn, PyData Xarray, Sphinx, Sympy, etc.) using official Docker execution containers.

| Metric | Kronumos 2 Kairos | Industry Multi-Turn Baselines |
| :--- | :---: | :---: |
| **Model Size** | **7B Parameters** | 70B - 405B / Frontier APIs |
| **Execution Mode** | **Single-Pass Zero-Shot** | Multi-Turn Agent Loop (50-100 Turns) |
| **Avg Tokens / Task** | **2,512 Tokens** | 40,000 - 150,000 Tokens |
| **Token Efficiency** | **93.5% Reduction** | Baseline (1.0x) |
| **API Cost** | **$0.00 (Pure Local Weights)** | $3.00 - $15.00 per issue |
| **Verified Resolved Tasks** | **8 Full Production Issues** | - |

### 🏆 Verified Resolved Production Issues:
1. `django__django-13569`: Broken aggregation expression logic in database queries.
2. `django__django-13658`: Management command argument parser collision.
3. `django__django-14855`: Admin URL generation prefix regression.
4. `django__django-15104`: Model custom key migration constraint hazard.
5. `django__django-16333`: Many-to-many relationship foreign key mapping.
6. `pydata__xarray-4629`: Multi-index coordinate slice dimension regression.
7. `scikit-learn__scikit-learn-10844`: Pipeline estimators parameter validation fault.
8. `sphinx-doc__sphinx-8595`: Python domain autodoc signature formatting error.

---

## 🔬 The Dual-Brain Cybernetic APR Architecture

Traditional LLM agents rely exclusively on multi-turn prompt loops, generating massive token overhead and hallucinating syntax formatting. Kronumos Kairos decouples cognition into two integrated computing cortices:

```
           [Raw GitHub Issue Discussion]
                         │
                         ▼
        ┌──────────────────────────────────┐
        │   Sub-Cortex IssueDeNoiser       │
        │   - Excises human chatter/quotes │
        │   - Tags user reproduction code  │
        │   - Extracts Core Signal Triad   │
        └────────────────┬─────────────────┘
                         │
        [Cleaned Technical Specification]
                         │
                         ▼
        ┌──────────────────────────────────┐
        │  Procedural Cognitive Kernel     │ ◄─── Procedural Seeds (<64 bytes)
        │  - BoundaryCondition Invariants  │      (Zero-DB L1 Cache Execution)
        │  - DefensiveNullWrap / PopGuards │
        └────────────────┬─────────────────┘
                         │
    ┌────────────────────┴────────────────────┐
    ▼                                         ▼
┌───────────────────────┐         ┌───────────────────────┐
│   CORTEX (Neural)     │         │ SUBCORTEX (Deterministic)
│  Qwen2.5-Coder-7B     │ ◄─────► │ Tree-sitter AST Slicer│
│  - 5-Step CoT Reason  │ Dual-Key│ Auto-Bracket & Indent │
│  - Precise Code Hunk  │ Consens.│ Merkle Causal Ledger  │
└───────────────────────┘         └───────────────────────┘
```

1. **Issue De-Noiser**: Strips human conversational chaff, extracting the core reproduction triad.
2. **Procedural Cognitive Kernel**: Diagnoses invariants across 9 domains (Boundary, Defensive, Concurrency, etc.) without external database lookups.
3. **Dual-Key Consensus Gate**: Requires simultaneous semantic approval and deterministic AST validation before admitting state changes.
4. **Auto-Bracket & Indentation Healer**: Deterministically balances parentheses and enforces strict PEP 8 4-space block indentation.

---

## ⚡ Native Rust Sub-Cortex Runtime

This repository includes the precompiled native Linux x86_64 binary `libtokenectomy_subcortex.so` and Python C-ABI bridge `tokenectomy_subcortex_rust.py`.

```python
from tokenectomy_subcortex_rust import RustSubCortex

subcortex = RustSubCortex()

# 1. Clean noisy issue descriptions (93.5% token reduction)
clean_spec = subcortex.denoise_issue(raw_github_issue)

# 2. Heal indentation drift and unbalanced brackets with sub-microsecond latency (5µs)
healed_code = subcortex.heal_indentation(candidate_code, base_indent=4)
```

---

## 💻 Quickstart: Running Inference

### With Transformers:
```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_id = "NadevA23/Kronumos-Kairos-v2"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

messages = [
    {"role": "system", "content": "You are Kronumos Kairos, an expert autonomous program repair engine."},
    {"role": "user", "content": "Fix the issue in the following function:\n\ndef safe_divide(a, b):\n    return a / b"}
]

inputs = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt").to(model.device)
outputs = model.generate(inputs, max_new_tokens=512, do_sample=False)
print(tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True))
```

### Quantized GGUF (Llama.cpp / Ollama):
For quantized local execution on consumer hardware, visit [NadevA23/Kronumos-Kairos-v2-GGUF](https://huggingface.co/NadevA23/Kronumos-Kairos-v2-GGUF).

---

## 📜 Citation

```bibtex
@article{daffa2026kronumos2,
  author    = {Muhammad Naufal Daffa},
  title     = {Kronumos 2 Kairos: Cost-Bounded Automated Program Repair via Dual-Brain Cybernetic Sub-Cortex on SWE-bench Verified},
  journal   = {Research Square},
  year      = {2026},
  doi       = {10.21203/rs.3.rs-11205335/v1},
  url       = {https://doi.org/10.21203/rs.3.rs-11205335/v1}
}
```

**License:** Apache 2.0  
**Maintained by:** Tokenectomy Labs
"""

# ==========================================
# 2. NadevA23/Kronumos-Kairos-v2-GGUF
# ==========================================
KAIROS_V2_GGUF_README = """---
base_model: NadevA23/Kronumos-Kairos-v2
tags:
- gguf
- llama.cpp
- ollama
- swe-bench
- autonomous-agents
- program-repair
- rust-subcortex
- dual-brain
license: apache-2.0
language:
- en
datasets:
- princeton-nlp/SWE-bench_Verified
pipeline_tag: reinforcement-learning
inference: false
---

# ⚡ Kronumos Kairos v2 (GGUF Quantized)

[![Springer Nature DOI](https://img.shields.io/badge/Springer_Nature-10.21203%2Frs.3.rs--11205335%2Fv1-00758f?style=flat-square&logo=springer&logoColor=white)](https://doi.org/10.21203/rs.3.rs-11205335/v1)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--7909--4916-A6CE39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0000-7909-4916)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Official GGUF quantized weights for **Kronumos 2 Kairos**, an open-weights cybernetic automated program repair engine evaluated on **Princeton SWE-bench Verified** (8 Officially Resolved Production Defects, 93.5% token reduction, $0 API cost).

- **Base Model (safetensors)**: [NadevA23/Kronumos-Kairos-v2](https://huggingface.co/NadevA23/Kronumos-Kairos-v2)
- **Preprint Paper**: Springer Nature Research Square ([DOI: 10.21203/rs.3.rs-11205335/v1](https://doi.org/10.21203/rs.3.rs-11205335/v1))
- **Author**: Muhammad Naufal Daffa ([ORCID: 0009-0000-7909-4916](https://orcid.org/0009-0000-7909-4916))
- **GitHub Repository**: [Tokenectomy-Labs/Kronomus](https://github.com/Tokenectomy-Labs/Kronomus)

---

## 💻 Running with Ollama

```bash
ollama run hf.co/NadevA23/Kronumos-Kairos-v2-GGUF
```

---

## 📜 Citation

```bibtex
@article{daffa2026kronumos2,
  author    = {Muhammad Naufal Daffa},
  title     = {Kronumos 2 Kairos: Cost-Bounded Automated Program Repair via Dual-Brain Cybernetic Sub-Cortex on SWE-bench Verified},
  journal   = {Research Square},
  year      = {2026},
  doi       = {10.21203/rs.3.rs-11205335/v1},
  url       = {https://doi.org/10.21203/rs.3.rs-11205335/v1}
}
```
"""

# ==========================================
# 3. NadevA23/Kronumos-14B-Kairos
# ==========================================
KAIROS_14B_README = """---
license: agpl-3.0
language:
- en
pipeline_tag: reinforcement-learning
inference: false
tags:
- code
- program-repair
- swe-bench
- autonomous-agent
- tokenectomy
- neuro-symbolic
- dual-brain
- rust-subcortex
base_model: Qwen/Qwen2.5-Coder-14B-Instruct
datasets:
- princeton-nlp/SWE-bench_Verified
---

# ⚡ Kronumos 14B Kairos (Experimental Checkpoint)

[![Springer Nature DOI](https://img.shields.io/badge/Springer_Nature-10.21203%2Frs.3.rs--11205335%2Fv1-00758f?style=flat-square&logo=springer&logoColor=white)](https://doi.org/10.21203/rs.3.rs-11205335/v1)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--7909--4916-A6CE39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0000-7909-4916)
[![Engine: 100% Native Rust C-ABI](https://img.shields.io/badge/Engine-100%25_Native_Rust_C--ABI-DEA584?style=flat-square&logo=rust)](https://github.com/Tokenectomy-Labs/Kronomus)

> [!NOTE]
> ### 🧪 SOVEREIGN EDGE APR ARCHITECTURE
> **Kronumos 14B Kairos** is the sovereign mid-scale model of the Kronumos Dual-Brain ecosystem, engineered to tackle complex algebraic, cross-module AST repairs (`sympy`, `sphinx`) with fast 1-turn self-healing.
> For cloud planetary scale, see [Kronumos Aion (671B MoE)](https://huggingface.co/NadevA23/Kronumos-Aion). For ultra-lightweight offline edge, see [Kronumos 2 Kairos (7B)](https://huggingface.co/NadevA23/Kronumos-Kairos-v2).

---

## 📌 Model Overview

**Kronumos 14B Kairos** is an autonomous software engineering model specialized for closed-loop program repair and automated bug remediation on production repositories.

- **Base Architecture:** Qwen2.5-Coder-14B-Instruct (bfloat16)
- **Primary Domain:** Automated Program Repair (APR) & Repository-Level Patch Synthesis
- **Target Benchmark:** Princeton SWE-bench Verified (500 instances)
- **Sub-Cortex Runtime:** Deterministic AST surgical engine written in Rust (**Tokenectomy C-ABI 5µs**)
- **Author & Research Lead:** Muhammad Naufal Daffa ([ORCID: 0009-0000-7909-4916](https://orcid.org/0009-0000-7909-4916)) | Tokenectomy Labs
- **Official Preprint:** Springer Nature Research Square — [DOI: 10.21203/rs.3.rs-11205335/v1](https://doi.org/10.21203/rs.3.rs-11205335/v1)
- **GitHub Repository:** [Tokenectomy-Labs/Kronomus](https://github.com/Tokenectomy-Labs/Kronomus)

---

## 🚀 Key Architectural Advantages Over Kronumos 7B

| Capability / Metric | Kronumos 7B | Kronumos 14B Kairos | Concrete Impact |
| :--- | :--- | :--- | :--- |
| **Parameter Scale** | 7.6 Billion | **14.7 Billion** | 2x capacity for abstract algorithmic and multi-hop reasoning |
| **Symbolic & Math Repos** | Struggled with deep algebraic trees | **Native Symbolic Mastery** | High candidate patch yield on challenging repos (`sympy`, `sphinx`) |
| **AST Self-Healing Velocity** | Required 3–4 turns to recover syntax | **Fast Turn 2 Self-Healing** | Recovers clean patches in 1 turn following Sub-Cortex compiler feedback |
| **Candidate Patch Yield** | ~72.4% yield | **85.8%+ yield** | Drastically higher rate of syntactically valid, testable git diffs |
| **Context Window Coherence** | 8,192 tokens | **16,384 – 32,768 tokens** | Holds whole-class inheritance hierarchies without attention degradation |
| **Hardware Marginal Cost** | ~0.12 Colab units / instance | **~0.19 Colab units / instance** | Remains strictly cost-bounded (~$5 total for 500 instances on A100) |

---

## ⚠️ Important Usage Notes

Kronumos is designed as a **cybernetic dual-brain architecture**:
1. The **14B Neural Core** generates candidate AST mutation hypotheses and targeted SEARCH/REPLACE blocks.
2. The **Tokenectomy Sub-Cortex (Rust)** validates full-file AST syntax, verifies relative indentation, and anchors patches to prevent dirty diffs.

```bash
git clone https://github.com/Tokenectomy-Labs/Kronomus.git
cd Kronomus
python3 scripts/kaggle_kronumos_runner.py --model_id NadevA23/Kronumos-14B-Kairos --bfloat16
```

---

## 📖 Citation

```bibtex
@article{daffa2026kronumos2,
  author    = {Muhammad Naufal Daffa},
  title     = {Kronumos 2 Kairos: Cost-Bounded Automated Program Repair via Dual-Brain Cybernetic Sub-Cortex on SWE-bench Verified},
  journal   = {Research Square},
  year      = {2026},
  doi       = {10.21203/rs.3.rs-11205335/v1},
  url       = {https://doi.org/10.21203/rs.3.rs-11205335/v1}
}
```

---
*Maintained by Tokenectomy Labs.*
"""

# ==========================================
# 4. NadevA23/Kronumos-14B-Kairos-GGUF
# ==========================================
KAIROS_14B_GGUF_README = """---
license: agpl-3.0
language:
- en
pipeline_tag: reinforcement-learning
inference: false
tags:
- gguf
- ollama
- code
- program-repair
- swe-bench
- tokenectomy
- dual-brain
- rust-subcortex
base_model: NadevA23/Kronumos-14B-Kairos
---

# ⚡ Kronumos 14B Kairos (GGUF Quantized Checkpoint)

[![Springer Nature DOI](https://img.shields.io/badge/Springer_Nature-10.21203%2Frs.3.rs--11205335%2Fv1-00758f?style=flat-square&logo=springer&logoColor=white)](https://doi.org/10.21203/rs.3.rs-11205335/v1)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--7909--4916-A6CE39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0000-7909-4916)

Official GGUF quantized weights for **Kronumos 14B Kairos**, an open-weights cybernetic automated program repair engine.

- **Base Model (safetensors)**: [NadevA23/Kronumos-14B-Kairos](https://huggingface.co/NadevA23/Kronumos-14B-Kairos)
- **Preprint Paper**: Springer Nature Research Square ([DOI: 10.21203/rs.3.rs-11205335/v1](https://doi.org/10.21203/rs.3.rs-11205335/v1))
- **Author**: Muhammad Naufal Daffa ([ORCID: 0009-0000-7909-4916](https://orcid.org/0009-0000-7909-4916))
- **GitHub Repository**: [Tokenectomy-Labs/Kronomus](https://github.com/Tokenectomy-Labs/Kronomus)

---

## 💻 Running with Ollama

```bash
ollama run hf.co/NadevA23/Kronumos-14B-Kairos-GGUF
```

---

## 📜 Citation

```bibtex
@article{daffa2026kronumos2,
  author    = {Muhammad Naufal Daffa},
  title     = {Kronumos 2 Kairos: Cost-Bounded Automated Program Repair via Dual-Brain Cybernetic Sub-Cortex on SWE-bench Verified},
  journal   = {Research Square},
  year      = {2026},
  doi       = {10.21203/rs.3.rs-11205335/v1},
  url       = {https://doi.org/10.21203/rs.3.rs-11205335/v1}
}
```
"""

# ==========================================
# 5. NadevA23/Kronumos
# ==========================================
KRONUMOS_OG_README = """---
license: apache-2.0
base_model: unsloth/Qwen2.5-Coder-7B-Instruct-bnb-4bit
tags:
  - code
  - autonomous-agent
  - bug-fix
  - self-healing
  - mcp
  - model-context-protocol
  - sre
  - tokenectomy
  - qwen2
  - unsloth
  - dual-brain
  - rust-subcortex
pipeline_tag: reinforcement-learning
inference: false
library_name: transformers
language:
  - en
---

# ⚡ Kronumos: The Dual-Brain Cybernetic Bug Remediation Engine

[![Springer Nature DOI](https://img.shields.io/badge/Springer_Nature-10.21203%2Frs.3.rs--11205335%2Fv1-00758f?style=flat-square&logo=springer&logoColor=white)](https://doi.org/10.21203/rs.3.rs-11205335/v1)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--7909--4916-A6CE39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0000-7909-4916)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**Kronumos** is the foundational release of the Kronumos Dual-Brain automated program repair ecosystem.

- **Current Active Release (v2.0)**: [NadevA23/Kronumos-Kairos-v2](https://huggingface.co/NadevA23/Kronumos-Kairos-v2)
- **14B Sovereign Edition**: [NadevA23/Kronumos-14B-Kairos](https://huggingface.co/NadevA23/Kronumos-14B-Kairos)
- **Titan Edition (671B MoE)**: [NadevA23/Kronumos-Aion](https://huggingface.co/NadevA23/Kronumos-Aion)
- **Official Preprint**: Springer Nature Research Square ([DOI: 10.21203/rs.3.rs-11205335/v1](https://doi.org/10.21203/rs.3.rs-11205335/v1))
- **Author**: Muhammad Naufal Daffa ([ORCID: 0009-0000-7909-4916](https://orcid.org/0009-0000-7909-4916))

---

## 📜 Citation

```bibtex
@article{daffa2026kronumos2,
  author    = {Muhammad Naufal Daffa},
  title     = {Kronumos 2 Kairos: Cost-Bounded Automated Program Repair via Dual-Brain Cybernetic Sub-Cortex on SWE-bench Verified},
  journal   = {Research Square},
  year      = {2026},
  doi       = {10.21203/rs.3.rs-11205335/v1},
  url       = {https://doi.org/10.21203/rs.3.rs-11205335/v1}
}
```
"""

TARGETS = [
    ("NadevA23/Kronumos-Kairos-v2", KAIROS_V2_README, True),
    ("NadevA23/Kronumos-Kairos-v2-GGUF", KAIROS_V2_GGUF_README, False),
    ("NadevA23/Kronumos-14B-Kairos", KAIROS_14B_README, True),
    ("NadevA23/Kronumos-14B-Kairos-GGUF", KAIROS_14B_GGUF_README, False),
    ("NadevA23/Kronumos", KRONUMOS_OG_README, False),
]

def main():
    print("🚀 Updating Hugging Face model cards for the Kronumos ecosystem...\n")
    for repo_id, readme_content, upload_binaries in TARGETS:
        print(f"📦 Processing: {repo_id}")
        try:
            # 1. Update README.md
            api.upload_file(
                path_or_fileobj=readme_content.encode("utf-8"),
                path_in_repo="README.md",
                repo_id=repo_id,
                repo_type="model",
                commit_message="Update model card: remove text-gen badge, add Springer Nature DOI, ORCID & Dual-Brain architecture"
            )
            print(f"  ✅ README.md updated successfully!")

            # 2. Upload binaries if applicable
            if upload_binaries:
                if os.path.exists(SO_PATH):
                    print(f"  📤 Uploading libtokenectomy_subcortex.so to {repo_id}...")
                    api.upload_file(
                        path_or_fileobj=SO_PATH,
                        path_in_repo="libtokenectomy_subcortex.so",
                        repo_id=repo_id,
                        repo_type="model",
                        commit_message="Add native Rust Sub-Cortex C-ABI binary (libtokenectomy_subcortex.so)"
                    )
                    print(f"  ✅ libtokenectomy_subcortex.so uploaded!")
                
                if os.path.exists(BRIDGE_PATH):
                    print(f"  📤 Uploading tokenectomy_subcortex_rust.py to {repo_id}...")
                    api.upload_file(
                        path_or_fileobj=BRIDGE_PATH,
                        path_in_repo="tokenectomy_subcortex_rust.py",
                        repo_id=repo_id,
                        repo_type="model",
                        commit_message="Add Python C-ABI bridge for Sub-Cortex"
                    )
                    print(f"  ✅ tokenectomy_subcortex_rust.py uploaded!")

        except Exception as e:
            print(f"  ❌ Error updating {repo_id}: {e}")

    print("\n🎉 Ecosystem model card update complete!")

if __name__ == "__main__":
    main()
