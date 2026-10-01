# Microsoft for Startups Founders Hub — Application Dossier
**Project:** Kronumos / Tokenectomy Labs  
**URL:** [https://foundershub.startups.microsoft.com/](https://foundershub.startups.microsoft.com/)  
**Stage:** Working Prototype / Pre-Seed  

---

## 1. Startup Basics

* **Company / Project Name:** Kronumos
* **Primary URL:** `https://github.com/Tokenectomy-Labs/Kronomus`
* **Country:** Indonesia
* **Stage:** Working Prototype / In-Development MVP
* **Funding:** Bootstrapped (Pre-Seed)
* **Team Size:** 3

---

## 2. Elevator Pitch & Problem Statement

### Elevator Pitch (1-2 sentences)
We build an automated bug-fixing engine that pairs a small, fine-tuned open model with a native Rust compiler extension. It cuts the token cost of fixing code issues by ~70% and prevents the indentation and git-apply rejections that break most LLM patches.

### What problem are you solving?
Most AI coding agents feed entire raw stack traces (often 80k to 150k tokens) into massive cloud models like Claude 3.5 Sonnet or GPT-4o. This burns $5 to $15 per issue and routinely fails on real repositories because LLMs struggle with precise whitespace, indentation, and AST syntax alignment when generating diffs. When the patch hits `git apply`, it fails before tests even run. 

On top of cost and syntax brittleness, banks, defense contractors, and fintech engineering teams cannot legally send proprietary source code to external closed-model APIs. There is no reliable, low-cost bug repair tool they can run locally inside their own infrastructure.

### How does your product solve this?
We split the task between a native compiler engine and a small neural model instead of forcing an LLM to do everything:

1. **Deterministic Rust Sub-Cortex:** Our native Rust library (`libtokenectomy_subcortex.so`, linked via C-ABI) parses the traceback, strips out framework noise (`node_modules`, `site-packages`), and slices the target AST function before the model runs. After generation, it heals block indentation and checks undeclared scopes in under 30 microseconds.
2. **Fine-Tuned Neural Cortex:** A specialized 8B/14B parameter open model that only reasons over the surgical repair logic, running unquantized on a single GPU.

By letting compiled Rust handle syntax and diff mechanics, we get clean, reproducible POSIX patches that actually apply cleanly in Docker test harnesses, while reducing token costs to under $0.05 per patch.

---

## 3. Market & Business Model

### Who is your target customer?
* **Fintech, Banking, and Defense Engineering Teams:** Teams with strict compliance constraints who need automated bug triage in CI/CD without leaking intellectual property outside their firewall.
* **Mid-to-Large Software Engineering Orgs:** Teams spending thousands of dollars monthly on AI developer seat licenses who want automated patch verification on regression issues before human review.
* **CI/CD Platform Integrators:** Developer tool platforms looking for a fast, headless bug-fixing engine.

### What is your business model?
* **Community Edition (Open Source):** Free open-weight 8B model and CLI for individual developers.
* **Enterprise Self-Hosted License ($40,000 – $80,000 / year):** B2B annual license for our air-gapped Rust binary, multi-language AST healing, and priority SLA for on-premise clusters.
* **Cloud API:** Pay-per-verified-patch endpoint for development teams running on cloud CI/CD.

---

## 4. How will you use Microsoft Azure compute credits?

We need Azure compute for three specific workloads:

1. **GPU Clusters (Azure ND A100 / NC A100 v4):** We currently benchmark on single-GPU instances. We need Azure A100 compute to train our next 14B and 32B model iterations and run 500-instance evaluation batches on Princeton's SWE-bench Verified suite.
2. **Parallel Docker Sandboxing (Azure Container Instances / AKS):** Evaluating SWE-bench requires spinning up hundreds of isolated containers with different Python/C environments to run repository test suites (`pytest`). Running these concurrently requires dedicated container capacity.
3. **GitHub Ecosystem Integration:** We want to deploy Kronumos as a native GitHub Action so engineering teams can automatically triage and draft pull requests for regression issues directly inside GitHub Enterprise.

---

## 5. Track Record & Verification Links

* **Research Lead:** Muhammad Naufal Daffa ([ORCID: 0009-0000-7909-4916](https://orcid.org/0009-0000-7909-4916))
* **Preprint on Springer Nature Portfolio (Research Square):** DOI: [`10.21203/rs.3.rs-11205335/v1`](https://doi.org/10.21203/rs.3.rs-11205335/v1) (*Kronumos 2 Kairos: Cost-Bounded Automated Program Repair via Dual-Brain Cybernetic Sub-Cortex on SWE-bench Verified*)
* **Permanent Archive on CERN Zenodo:** DOI: [`10.5281/zenodo.22929676`](https://doi.org/10.5281/zenodo.22929676)
* **Open Weights on Hugging Face:** [`NadevA23/Kronumos`](https://huggingface.co/NadevA23/Kronumos)
* **Open Source Repository:** [`Tokenectomy-Labs/Kronomus`](https://github.com/Tokenectomy-Labs/Kronomus)
