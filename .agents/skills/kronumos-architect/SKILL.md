---
name: kronumos-architect
description: >-
  Essential architecture guide and autonomous invariants for Kronumos Kairos and Tokenectomy engines.
  Covers the dual Sub-Cortex architecture, engine tiering (OSS, Pro, Sovereign), Cloudflare edge gateway,
  terminal typography invariants, token conservation guards, platform distribution, and air-gapped private tier isolation.
---

# Kronumos Kairos & Tokenectomy Architecture Skill

This skill defines the permanent architectural invariants, engine hierarchy, security protocols, and operational workflows for Kronumos Kairos and the Tokenectomy Sub-Cortex. Any AI assistant working on this codebase must follow these principles without exception.

## 1. Founder & Identity Context
* **Creator / Entity**: Tokenectomy Labs.
* **Founder Relationship**: The user is the founder, architect, and creator of the entire Tokenectomy engine ecosystem and Kronumos. Never lecture or talk down to the user; provide senior-level peer engineering collaboration.
* **Name & Role**: Kronumos Kairos is an autonomous code remediation and SRE agent, fine-tuned specifically for closed-loop TDD bug repair, not a generic conversational chatbot.

## 2. Dual-Architecture Paradigm (Sub-Cortex + Reasoning Model)
Kronumos does NOT feed raw terminal dumps to LLMs. It operates on a strict two-layer architecture:
1. **Sub-Cortex (Local Native Rust Engine - Tokenectomy)**:
   * Executes deterministically in microseconds on the user machine.
   * `tokenectomy::extractor::extract_context`: Pinpoints failing files and line numbers across 9 programming languages (Python, Rust, JS/TS, Go, Java, C++, PHP, Ruby, C#) and extracts 15 lines of offending source code context.
   * `tokenectomy::extractor::prune_framework_noise`: Strips internal framework frames (`site-packages`, `node_modules`, standard libraries), achieving 91.3% token reduction.
   * `tokenectomy::redact_secrets`: Client-side sanitization of JWTs, AWS keys, GitHub tokens, and database passwords before anything leaves the machine.
2. **Inference Cortex (Edge Reasoning)**:
   * Hosted on Cloudflare Workers AI via the Kronumos Gateway (`https://kronumos-gateway.tokenectomysupport.workers.dev`).
   * Primary Model: `@cf/qwen/qwen2.5-coder-32b-instruct` (high-accuracy AST reasoning).
   * Automated Failover: `@cf/meta/llama-3.1-8b-instruct-fast` (instant fallback if Qwen 32B encounters GPU capacity spikes or timeouts).
   * Offline / Air-Gapped Mode: Local Ollama GGUF model `hf.co/NadevA23/Kronumos-GGUF:Q4_K_M`.

## 3. Engine Tiering Hierarchy (OSS vs Pro vs Sovereign)
The user developed three tiers of the Tokenectomy engine:
* **Tier 1: OSS (Open Source)**:
  * Crate: `Tokenectomy-OSS` (`tokenectomy v1.3.3`).
  * Used in the public open-source binary of Kronumos (`Tokenectomy-Labs/Kronomus`).
  * Features: 9-language traceback parsing, framework noise pruning, secret scrubbing.
* **Tier 2: Pro (Intermediate)**:
  * Extended diagnostic probes: database connection starvation, container crash inspection (exit code 137 OOMKilled), and AST patch application verification.
* **Tier 3: Sovereign / Ultra (Apex)**:
  * Internal sovereign state machine: zero-LLM AST repair, immune cluster matching, speculative evolution, backward slicing.
  * **Strict Air-Gap Rule**: Sovereign tools must remain strictly isolated inside local-only crates (`publish = false`, 0 Git remotes, local commits only). NEVER reference, leak, or import sovereign crates into public repositories (`web anonim` / `Tokenectomy-Labs/Kronomus`).

## 4. Repository Split & Air-Gap Boundary
* **Public Repository (`/home/nans/web anonim`)**:
  * GitHub Remote: `https://github.com/Tokenectomy-Labs/Kronomus.git` (Branch `main`).
  * Contents: Public documentation, GitHub Action (`action.yml`), installer scripts (`cli/install.sh`, `cli/install.ps1`), Cloudflare gateway (`gateway/`), and official website (`index.html`).
* **Private Core Repository (`/home/nans/Tokenonmix/Kronumos-Core`)**:
  * Air-gapped Rust repository.
  * Invariant: `git remote -v` must remain empty. Never add external Git remotes. Local commits only.
  * Binary packaging: `./build_release.sh` creates stripped release binaries in `dist/`.

## 5. Hard Autonomous Behavioral Invariants
* **Terminal Typography Invariant**:
  * Never output raw markdown asterisks (`*`, `**`) or backslash-escaped quotes in conversational terminal chat.
  * The terminal stream filter in `Kronumos-Core` strips them in real-time. Keep all agent prose natural and clean. Executable triple-backtick code blocks and math symbols (`5 * 10`) must remain untouched.
* **Token Conservation & Permission Gate**:
  * `view_file` is strictly clamped to a maximum of 100 lines per call with Sub-Cortex pagination notice.
  * `list_files` is strictly clamped to 40 items and max depth 3.
  * The agent must never perform blind exploratory scans of project roots. It must ask the user for permission or target scope first.
* **No Horizontal Rules Invariant**:
  * Never use horizontal rules (`---` or `<hr>`) in assistant responses.
* **No Marketing AI Slop**:
  * Never use generic AI design clichés: no cyan/purple neon glow blobs, no pulsating circles, no cookie-cutter emoji cards.
  * The official web portal uses a **Refined Brushed Titanium & Industrial Chrome** aesthetic.
  * Do NOT put an interactive playground on the landing page: users must be channeled toward downloading the real tool.

## 6. Multi-Platform Distribution Reference
* **Official Website**: `https://tokenectomy-labs.github.io/Kronomus/`
* **Linux (GUI Users)**:
  * File: `kronumos_1.0.0_amd64.deb` (uploaded to GitHub Releases v1.0.0).
  * Double-click in File Manager and click Install on Ubuntu, Debian, Mint, Pop!_OS.
* **Linux (CLI Users)**:
  * `curl -fsSL https://raw.githubusercontent.com/Tokenectomy-Labs/Kronomus/main/cli/install.sh | bash`
* **Windows (PowerShell / WSL 2)**:
  * PowerShell 1-liner: `irm https://raw.githubusercontent.com/Tokenectomy-Labs/Kronomus/main/cli/install.ps1 | iex`
  * WSL 2 is the recommended path for running Linux test runners (`pytest`, `cargo`, `npm`, `docker`) natively on Windows.
* **Cryptographic Verification**:
  * Windows: `certutil -hashfile kronumos_1.0.0_amd64.deb SHA256`
  * Linux: `sha256sum -c kronumos_1.0.0_amd64.deb.sha256`

## 7. Cloudflare Gateway Runbook
* **Directory**: `/home/nans/web anonim/gateway`
* **Worker**: `worker.js`, configuration in `wrangler.toml`.
* **Deployment**: Run `npm run deploy` inside `gateway/`.
* **Health Check**: `curl -sI https://kronumos-gateway.tokenectomysupport.workers.dev/health`
* **Inference Endpoint**: `POST /v1/chat/completions` (OpenAI-compatible schema with SSE streaming).
* **Guards**: 128KB payload cap, 6 req/10s burst limit, 30 req/h sliding window per IP, edge secret redaction, automatic failover header `X-Kronumos-Fallback: true/false`.
