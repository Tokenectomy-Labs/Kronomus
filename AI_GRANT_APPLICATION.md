# AI Grant Application Dossier — Kronumos & Tokenectomy
**Target Program:** AI Grant (Nat Friedman & Daniel Gross)  
**Round:** Pre-Seed Uncapped MFN SAFE ($250k Cash + $350k Azure + $250k Partner Compute)  
**Date:** October 2026  

---

### 1. Company & Project Info
* **Company Name:** Kronumos Inc. (Tokenectomy Labs)
* **Code Repository:** `https://github.com/Tokenectomy-Labs/Kronomus`
* **Founders:**
  * CTO (AI & Systems Architect): Muhammad Naufal Daffa ([ORCID: 0009-0000-7909-4916](https://orcid.org/0009-0000-7909-4916))
  * CEO (Commercial & Business Lead)
  * CPO (Frontend & Developer Experience Lead)
* **Scholarly Records & Preprints:**
  * Springer Nature Portfolio (Research Square): DOI [`10.21203/rs.3.rs-11205335/v1`](https://doi.org/10.21203/rs.3.rs-11205335/v1)
  * CERN Zenodo Permanent Archive: DOI [`10.5281/zenodo.22929676`](https://doi.org/10.5281/zenodo.22929676)
  * Open Weights: [`NadevA23/Kronumos`](https://huggingface.co/NadevA23/Kronumos)

---

### 2. What are you building? (1-2 sentences)
We build Kronumos, an automated code repair engine that splits bug fixing between a fine-tuned open model and a native Rust compiler. It drops the token cost of fixing GitHub issues by ~95% ($0.05 vs $10.00 per patch) while preventing the whitespace and syntax errors that cause most LLM patches to fail `git apply`.

---

### 3. What is your unfair advantage? Why will you win against Devin / Claude / Copilot?
1. **The Context Bloat Wall:** Existing agents feed entire 80k-to-150k token tracebacks directly into closed LLM APIs. This costs $5 to $15 per issue and hallucinates minor indentations on real codebases.
2. **Compiler-First Architecture:** Our native Rust library (`libtokenectomy_subcortex.so`, linked via C-ABI) cleans the traceback and slices the target AST function before the model runs. After inference, it normalizes block indentation and checks undeclared scopes in 5 to 30 microseconds without burning model tokens.
3. **True Air-Gapped Deployment:** Regulated industries (banking, defense, healthcare) cannot send internal proprietary code to US closed-cloud APIs. Kronumos runs fully self-hosted on a single GPU node.

---

### 4. Technical Architecture
```
[Bug Report / Traceback]
        │
        ▼
[Rust Sub-Cortex (5 µs C-ABI)] ──► Strips 70% trace noise, extracts AST target function
        │
        ▼
[Kronumos 8B Neural Cortex]    ──► Generates surgical logic patch (bfloat16)
        │
        ▼
[Rust IndentationHealer]       ──► Enforces POSIX diff compliance before git apply
        │
        ▼
[Clean Git Patch Applied]
```

* **Core Engine:** Written in Rust (`crates/tokenectomy-subcortex`), exposed via C-ABI dynamic linking.
* **Inference:** Runs in unquantized `bfloat16` on a single NVIDIA A100/A10G, or 4-bit quantized locally.
* **POSIX Git Integration:** Fixes indentation headers deterministically so candidate patches apply cleanly in Docker test harnesses.

---

### 5. What milestones have you achieved so far?
* **Springer Nature Preprint:** Indexed research preprint with permanent DOI on Research Square.
* **Compiled Native Engine:** Built sub-microsecond Rust compiler components (`IndentationHealer`, `ScopeGuard`, `SentinelAudit`) with verified C-ABI integration.
* **SWE-bench Verified Pipeline:** Built an end-to-end Docker benchmark runner that tests candidate patches against official repository pytest suites without fake line-1 diff fallbacks.
* **Public Model Release:** Shipped fine-tuned open weights on Hugging Face (`NadevA23/Kronumos`).

---

### 6. Team Background
* **CTO (Systems & AI):** Designed the Rust Sub-Cortex and fine-tuned the Kronumos neural checkpoints. Background in systems programming, C-ABI FFI, and PyTorch inference optimization.
* **CEO (Commercial & Sales):** Leads enterprise customer discovery (banking, fintech), grant applications, and corporate partnerships.
* **CPO (Product & UI):** Leads developer experience, web interfaces, and interactive token telemetry dashboards.

---

### 7. How will the $250k cash and compute credits be used?
* **$250k Cash:** 
  * 18-month runway for the 3 core founders.
  * Formal Delaware C-Corp incorporation via Stripe Atlas, trademark registration, and corporate banking.
  * Enterprise pilot customer acquisition and customer discovery.
* **Compute Credits ($350k Azure + $250k Partners):**
  * Train our next 14B and 32B model iterations across multi-GPU clusters.
  * Run continuous 500-issue SWE-bench Verified batch evaluations in parallel Docker containers.
