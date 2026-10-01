#!/usr/bin/env python3
"""
⚡ Publish Official Kronumos AI Organization Card
=================================================
Automates publishing the official Kronumos AI profile card to Kronumos/README space.
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
api = HfApi(token=TOKEN)
REPO_ID = "Kronumos/README"

ORG_CARD_CONTENT = """---
title: Kronumos AI
emoji: 🏛️
colorFrom: blue
colorTo: indigo
sdk: static
pinned: false
---

<div align="center">

<img src="https://raw.githubusercontent.com/Tokenectomy-Labs/Kronomus/main/assets/kronumos_logo.png" alt="Kronumos AI" width="340" />

# 🏛️ Kronumos Cybernetics (Kronumos AI)
### Deterministic Dual-Brain Autonomous Program Repair & Systems Engineering

[![Springer Nature DOI](https://img.shields.io/badge/Springer_Nature-10.21203%2Frs.3.rs--11205335%2Fv1-00758f?style=flat-square&logo=springer&logoColor=white)](https://doi.org/10.21203/rs.3.rs-11205335/v1)
[![ORCID](https://img.shields.io/badge/ORCID-0009--0000--7909--4916-A6CE39?style=flat-square&logo=orcid&logoColor=white)](https://orcid.org/0009-0000-7909-4916)
[![Sub-Cortex: 100% Native Rust](https://img.shields.io/badge/Sub--Cortex-100%25_Native_Rust_(5µs)-DEA584?style=flat-square&logo=rust)](https://github.com/Tokenectomy-Labs/Kronomus)
[![Benchmark: SWE-bench Verified](https://img.shields.io/badge/Benchmark-SWE--bench_Verified-success?style=flat-square)](https://huggingface.co/datasets/princeton-nlp/SWE-bench_Verified)

<p align="center">
  <a href="https://doi.org/10.21203/rs.3.rs-11205335/v1"><b>[📄 Research Preprint]</b></a> •
  <a href="https://github.com/Tokenectomy-Labs/Kronomus"><b>[💻 GitHub Repository]</b></a> •
  <a href="https://github.com/Tokenectomy-Labs/Kronomus/blob/main/LICENSE_ENTERPRISE.md"><b>[⚖️ Enterprise Terms]</b></a>
</p>

</div>

---

### 🔬 About Kronumos AI
**Kronumos AI** is a cybernetic artificial intelligence research and systems engineering organization developing deterministic **Dual-Brain foundation models** and autonomous program repair systems. 

By coupling large-scale mixture-of-experts cognitive cortices with native microsecond Rust compiler Sub-Cortex kernels (`libtokenectomy_subcortex.so`, C-ABI 5µs latency), Kronumos **eliminates 93.5% of context token bloat** and guarantees **100% zero-dirty-diff repairs** on production software monorepos.

---

### 🚀 Production Model Portfolio

| Model | Architecture | Parameters | Target Workload | Access |
| :--- | :--- | :---: | :--- | :--- |
| 🏛️ [**Kronumos Aion**](https://huggingface.co/Kronumos/Kronumos-Aion) | MoE Dual-Brain | **671B** | Planetary-scale multi-hop enterprise repair | [Explore Model](https://huggingface.co/Kronumos/Kronumos-Aion) |
| ⚡ [**Kronumos 2 Kairos**](https://huggingface.co/Kronumos/Kronumos-Kairos-v2) | Dense Distilled | **7.6B** | High-velocity local dev & offline CI/CD | [Explore Model](https://huggingface.co/Kronumos/Kronumos-Kairos-v2) |
| 💻 [**Kronumos 14B Kairos**](https://huggingface.co/Kronumos/Kronumos-14B-Kairos) | Sovereign Dense | **14.7B** | Complex algebraic & symbolic AST remediation | [Explore Model](https://huggingface.co/Kronumos/Kronumos-14B-Kairos) |

---

### ⚡ Core Engineering Invariants
1. **Sub-Microsecond Determinism**: Native Rust C-ABI execution with 5µs Tree-sitter AST indentation and scope verification.
2. **Context Efficiency**: 93.5% reduction in input token bloat via deterministic Issue De-Noising.
3. **Hardware-Grounded Truth**: Rigorously benchmarked on **Princeton SWE-bench Verified** with official Docker pytest execution containers.

---

### 📖 Citation & Research Provenance
```bibtex
@article{daffa2026kronumos,
  title     = {Kronumos 2 Kairos: Cost-Bounded Automated Program Repair via Dual-Brain Cybernetic Sub-Cortex on SWE-bench Verified},
  author    = {Muhammad Naufal Daffa},
  journal   = {Springer Nature Research Square},
  year      = {2026},
  doi       = {10.21203/rs.3.rs-11205335/v1},
  url       = {https://doi.org/10.21203/rs.3.rs-11205335/v1}
}
```

* **Author & Research Lead:** Muhammad Naufal Daffa ([ORCID: 0009-0000-7909-4916](https://orcid.org/0009-0000-7909-4916))  
* **Organization:** Tokenectomy Labs
"""

def main():
    print(f"🚀 Authoring Organization Card for {REPO_ID}...")
    try:
        # Step 1: Open PR with the Organization Card
        res = api.upload_file(
            path_or_fileobj=ORG_CARD_CONTENT.encode("utf-8"),
            path_in_repo="README.md",
            repo_id=REPO_ID,
            repo_type="space",
            create_pr=True,
            commit_message="docs: author official Kronumos AI organization profile card"
        )
        print("  ✅ PR Created:", res)
        
        # Step 2: Discover PR number
        discussions = list(api.get_repo_discussions(REPO_ID, repo_type="space"))
        target_pr = None
        for d in discussions:
            if d.status == "open":
                target_pr = d.num
                break
        
        if not target_pr:
            print("  ⚠️ Could not find open PR number!")
            return

        print(f"  🔍 Found open PR #{target_pr}. Merging directly...")
        api.merge_pull_request(repo_id=REPO_ID, discussion_num=target_pr, repo_type="space")
        print(f"  🎉 SUCCESS! PR #{target_pr} merged! Organization card is LIVE!")

    except Exception as e:
        print("  ❌ Error:", e)

if __name__ == "__main__":
    main()
