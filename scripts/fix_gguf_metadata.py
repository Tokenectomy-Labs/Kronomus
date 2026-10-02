import os
from huggingface_hub import HfApi

# Read HF token from .env
token = None
if os.path.exists(".env"):
    with open(".env", "r") as f:
        for line in f:
            if line.startswith("HF_TOKEN="):
                token = line.strip().split("=", 1)[1].strip("\"'")

if not token:
    raise ValueError("HF_TOKEN not found in .env")

api = HfApi(token=token)

content = """---
base_model: Kronumos/Kronumos-Kairos-v2
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
pipeline_tag: text-generation
inference: false
---

# ⚡ Kronumos Kairos v2 (GGUF Quantized)

[![Springer Nature DOI](https://img.shields.io/badge/Springer_Nature-10.21203%2Frs.3.rs--11205335%2Fv1-00758f?style=flat-square&logo=springer&logoColor=white)](https://doi.org/10.21203/rs.3.rs-11205335/v1)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--7909--4916-A6CE39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0000-7909-4916)
[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Official GGUF quantized weights for **Kronumos Kairos v2**, an open-weights cybernetic automated program repair engine evaluated on **Princeton SWE-bench Verified** (8 Officially Resolved Production Defects, 93.5% token reduction, $0 API cost).

- **Base Model (safetensors)**: [Kronumos/Kronumos-Kairos-v2](https://huggingface.co/Kronumos/Kronumos-Kairos-v2)
- **Preprint Paper**: Springer Nature Research Square ([DOI: 10.21203/rs.3.rs-11205335/v1](https://doi.org/10.21203/rs.3.rs-11205335/v1))
- **Author**: Muhammad Naufal Daffa ([ORCID: 0009-0000-7909-4916](https://orcid.org/0009-0000-7909-4916))
- **GitHub Repository**: [Tokenectomy-Labs/Kronomus](https://github.com/Tokenectomy-Labs/Kronomus)

---

## 💻 Running with Ollama

```bash
ollama run hf.co/Kronumos/Kronumos-Kairos-v2-GGUF
```

## 🛠️ Running with llama.cpp

```bash
llama-cli -m Kronumos-Kairos-v2-Q4_K_M.gguf -p "<|im_start|>system\\nYou are Kronumos Kairos, an autonomous program repair engine.<|im_end|>\\n<|im_start|>user\\nAnalyze and fix the regression.<|im_end|>\\n<|im_start|>thought\\n"
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

repo_id = "Kronumos/Kronumos-Kairos-v2-GGUF"

print(f"Updating {repo_id}...")
try:
    # First try direct commit
    api.upload_file(
        path_or_fileobj=content.encode("utf-8"),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="model",
        commit_message="Fix pipeline_tag to text-generation to eliminate video preview bug and update org links",
        create_pr=False
    )
    print("SUCCESS: Committed directly to repo!")
except Exception as e:
    print(f"Direct commit failed ({e}), creating PR...")
    pr = api.upload_file(
        path_or_fileobj=content.encode("utf-8"),
        path_in_repo="README.md",
        repo_id=repo_id,
        repo_type="model",
        commit_message="Fix pipeline_tag to text-generation to eliminate video preview bug and update org links",
        create_pr=True
    )
    print(f"SUCCESS: PR created: {pr}")
