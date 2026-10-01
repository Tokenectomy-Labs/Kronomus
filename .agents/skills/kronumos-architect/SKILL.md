---
name: kronumos-architect
description: >-
  Comprehensive end-to-end architecture, technical, research, and business roadmap for Kronumos & Tokenectomy.
  Ingests the complete foundation from upstream AST parsing and native Rust Sub-Cortex (C-ABI 5µs) to
  Princeton SWE-bench Verified Docker evaluation, Springer Nature preprint provenance, and investor term sheets.
---

# 🧭 Kronumos & Tokenectomy: Master Architecture & Ecosystem Skill

This skill is the permanent, authoritative knowledge base for **Kronumos & Tokenectomy**. Any AI agent (Antigravity, Claude, Cursor, Cline, Roo Code, Windsurf) entering this workspace MUST read this document to understand the full system from upstream (hulu) to downstream (hilir) without requiring the founder to re-explain.

---

## 👤 1. Founder & Team Structure

### Founder Identity
* **Founder & Research Lead:** Muhammad Naufal Daffa ([ORCID: 0009-0000-7909-4916](https://orcid.org/0009-0000-7909-4916)).
* **Role:** Lead AI & Systems Architect / Chief Technology Officer (CTO).
* **Location:** Bima, Indonesia.
* **Collaboration Persona:** Treat the founder with high respect as a brilliant systems engineer and peer researcher. Never talk down, lecture, or generate patronizing summaries.

### The Trio Founding Team & Cap Table (`FOUNDER_ACCORD_TERM_SHEET.md`)
1. **The Hacker (CTO - Naufal):** **50% Equity**. Creator of Rust Sub-Cortex, Qwen neural fine-tuning, AST parser, and scientific papers.
2. **The Hustler (CEO - Commercial Lead):** **30% Equity**. Manages grant submissions (Microsoft, AI Grant), B2B enterprise sales, investor relations.
3. **The Hipster (CPO - Frontend Lead):** **20% Equity**. Builds the official web portal, interactive token calculator, and developer experience.
* **Standard Invariants:** **4-Year Vesting with 1-Year Cliff**. Full IP Assignment (PIIA) to **Kronumos Inc.** (Delaware C-Corp via Stripe Atlas).

---

## 🧠 2. Core Dual-Cortex Architecture (Hulu ke Hilir)

Kronumos rejects the "monolithic prompt wrapper" approach of Devin and Claude. It decouples automated code repair into a neurosymbolic pipeline:

```
[Issue / Traceback]
        │
        ▼
[1. Tokenectomy Rust Sub-Cortex] ──► Excises 70-95% trace noise in 5 µs (C-ABI)
        │                            Parses Python import statements (`from x.y import z`)
        │                            Extracts exact AST target function body & line number
        ▼
[2. Kronumos Neural Cortex]      ──► Fine-tuned Qwen2.5-Coder (8B / 14B) in bfloat16
        │                            Generates minimal surgical repair logic
        ▼
[3. Symbolic Healing & Guard]    ──► `IndentationHealer`: 5 µs block rebasing with relative indent
        │                            `ScopeGuard`: 30 µs undeclared identifier & NameError check
        ▼
[4. Clean POSIX Git Diff]        ──► 100% passes `git apply` cleanly in Princeton Docker Pytest harness
```

### Key Technical Artifacts:
* **Compiled Native Library:** `crates/tokenectomy-subcortex/target/release/libtokenectomy_subcortex.so` (2.8 MB, C-ABI FFI with `#[no_mangle] extern "C"`).
* **Fault Localization Engine:** `scripts/kaggle_kronumos_runner.py` (has `extract_suspect_context_from_issue` with AST module import parsing; captures definitions like `separability_matrix` line 66 on `astropy-12907`).
* **Zero-Mock Invariant (CRITICAL):** Absolutely NO synthetic fallbacks or line-1 diff hacks (`@@ -1,1`). If a file is unverified, report an honest error. Honest failure is infinitely preferred over hallucinated diffs.

---

## 📜 3. Academic & Scientific Provenance

Kronumos is backed by formal, timestamped international research credentials:
* **Springer Nature Portfolio (Research Square):**  
  Title: *Kronumos 2 Kairos: Cost-Bounded Automated Program Repair via Dual-Brain Cybernetic Sub-Cortex on SWE-bench Verified*  
  DOI: [`10.21203/rs.3.rs-11205335/v1`](https://doi.org/10.21203/rs.3.rs-11205335/v1)
* **CERN Zenodo Permanent Archive:**  
  DOI: [`10.5281/zenodo.22929676`](https://doi.org/10.5281/zenodo.22929676)
* **Open Model Weights:** Hugging Face [`NadevA23/Kronumos`](https://huggingface.co/NadevA23/Kronumos)
* **Live Interactive Workbench:** Hugging Face Spaces [`NadevA23/Kronumos-2-Kairos`](https://huggingface.co/spaces/NadevA23/Kronumos-2-Kairos)

---

## 💼 4. Business & Investor Roadmap

### A. Active Grants & Applications
1. **Microsoft for Startups Founders Hub:**
   * Dossier: [`MICROSOFT_FOR_STARTUPS_APPLICATION.md`](file:///home/nans/web%20anonim/MICROSOFT_FOR_STARTUPS_APPLICATION.md).
   * Benefit: Up to **$150,000 Azure GPU Credits** (ND A100 / NC A100 v4) + GitHub Enterprise.
   * Terms: **0% Equity (Non-dilutive)**, 100% founder IP ownership.
2. **AI Grant (Nat Friedman - Ex-CEO GitHub & Daniel Gross):**
   * Dossier: [`AI_GRANT_APPLICATION.md`](file:///home/nans/web%20anonim/AI_GRANT_APPLICATION.md).
   * Benefit: **$250,000 CASH TUNAI DI REKENING BANK** + $350k Azure + $250k partner credits (Modal, Anthropic, Replicate).
   * Terms: **Uncapped MFN SAFE (~7% - 8% equity dilution)**, NO board seat, NO debt, 0 personal liability.

### B. Valuation Framework
* **Hard Asset Replacement Floor:** **Rp 3.500.000.000,- ($220k USD)** (Cost of Senior Rust + ML Engineers + GPU clusters).
* **Pre-Seed Market Valuation (SAFE):** **Rp 47 – 55 Miliar ($3.0M – $3.5M USD)** based on $250k for ~7% equity.
* **Series A Target:** **$30M – $50M USD** upon securing 3-5 bank/fintech B2B on-premise contracts ($50k/year each).

---

## 📁 5. Directory & Repository Map

* **Public Core Repo (`/home/nans/web anonim`):**
  * `crates/tokenectomy-subcortex/`: Rust source code for the Sub-Cortex engine.
  * `scripts/kaggle_kronumos_runner.py`: End-to-end SWE-bench runner with AST fault localization.
  * `colab_kronumos_8b_a100.ipynb`: Official Google Colab A100 execution notebook.
  * `MICROSOFT_FOR_STARTUPS_APPLICATION.md`: Polished, authentic application for Azure Founders Hub.
  * `AI_GRANT_APPLICATION.md`: Polished, authentic application for AI Grant $250k cash.
  * `FOUNDER_ACCORD_TERM_SHEET.md`: 50/30/20 equity split and 4-year vesting agreement.
  * `CPO_FRONTEND_SPEC.md`: Product brief for landing page and interactive token calculator.
  * `HUGGINGFACE_MODEL_CARD.md`: Model card with Springer Nature DOI and ORCID badges.
* **Private Sovereign Core (`/home/nans/Tokenonmix/Kronumos-Core`):**
  * Rule 9 Invariant: Strict local-only isolation. `git remote -v` remains empty. Never leak sovereign crates into public repos.

---

## ⚙️ 6. Operational Invariants for AI Agents

1. **Token Surgery First:** Never feed massive raw logs to LLMs without scrubbing via Tokenectomy.
2. **Authentic Voice (No AI Slop):** Avoid corporate buzzwords (*delve, revolutionize, leverage, seamless, paradigm shift*). Keep engineering prose direct, humble, and grounded.
3. **Hardware Grounding:** Always verify performance claims against physical execution (C-ABI tests, Docker pytest).
4. **Partner Execution:** Support Naufal as the technical anchor, keeping focus on model accuracy and systems architecture while delegating business/UI to the team dossiers.
