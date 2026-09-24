# ⚡ Kronumos CLI — Autonomous Bug Remediation Agent

An agentic terminal REPL powered by **Kronumos Core** and the **Tokenectomy Rust Sub-Cortex**. Designed with a minimalist, transparent-terminal aesthetic for pair-debugging, continuous test verification, and automated root-cause healing.

```text
    ██╗  ██╗██████╗  ██████╗ ███╗   ██╗██╗   ██╗███╗   ███╗ ██████╗ ███████╗
    ██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██║   ██║████╗ ████║██╔═══██╗██╔════╝
    █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║   ██║██╔████╔██║██║   ██║███████╗
    ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██║╚██╔╝██║██║   ██║╚════██║
    ██║  ██╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝███████║
    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚══════╝

                     · K R O N U M O S   K A I R O S ·
               Autonomous Code Remediation & SRE Agent • v1.0
```


## ⚡ Installation

### Option 1: Cargo Install (Recommended)
```bash
cargo install --git https://github.com/Tokenectomy-Labs/Tokenectomy --bin kronumos
```

### Option 2: 1-Line Installer
```bash
curl -fsSL https://raw.githubusercontent.com/Tokenectomy-Labs/Kronomus/main/cli/install.sh | bash
```


## 🚀 Usage Modes

### 1. Autonomous TDD Self-Healing Loop (Headless CI/CD)
Point Kronumos at any workspace. It automatically detects the project build system (`cargo`, `pytest`, `npm test`, `go test`), probes test baselines, excises noise and sensitive credentials via Sub-Cortex, synthesizes surgical AST patches, and verifies that tests pass on real hardware before completing:
```bash
# Run autonomous self-healing loop until green
kronumos --loop

# Or use the --fix alias with custom workspace
kronumos --fix --workspace /path/to/repo

# Auto-rollback on failure (guarantees 0 dirty diff if loop cannot resolve all tests)
kronumos --loop --auto-rollback

# Auto Git Delivery: automatically branch and commit verified patch once tests pass
kronumos --loop --branch fix/auth-race --commit

# Machine-to-Machine JSON output for CI/CD pipelines
kronumos --loop --json
```
* **Semantic Exit Codes**: Exits with code `0` on verified test pass, or code `1` if failures remain unresolved after max iterations.

### 2. One-Shot Positional Execution
Ask questions or request code audits directly from your terminal without entering the interactive shell:
```bash
kronumos "Analyze src/auth.rs and identify potential race conditions"
kronumos "Explain the blast radius of refactoring UserSession"
```

### 3. Unix Pipeline & Headless Piping
Pipe compiler errors, stack traces, or container logs directly into Kronumos with quiet mode (`-q / --quiet`) to strip visual banners and spinners:
```bash
cat cargo_build.log | kronumos -q
pytest 2>&1 | kronumos -q "Diagnose and fix these failing assertions"
docker logs app_container 2>&1 | kronumos -q "Identify root cause of OOM crash"
```

### 4. Interactive Agent Cockpit (Antigravity-Grade Terminal UX)
Launch directly into the ambient, transparent-terminal pair-debugging cockpit styled with Kronumos Kairos design, live animated spinners, framed tool execution cards, and visual diffs:
```bash
kronumos
```
* **Live Animated Spinners**: Real-time cyan spinners (`⠋⠙⠹...`) while querying Sub-Cortex, streaming tokens, or executing test suites.
* **Framed Tool Cards**: Visual status cards for `run_command`, `apply_patch`, `write_file`, `search_code`, `view_file`, and `git_action` with `[✓ exit 0]` and `[✗ exit 1]` badges.
* **Direct Shell Escape (`!<cmd>`)**: Run shell commands directly on physical hardware with zero token consumption and zero LLM latency (e.g. `!cargo test`, `!git status`).
* **Interactive File Mentions (`@<file>`)**: Press Tab after `@` to autocomplete project files; auto-inlines file content into model context.
* **Multi-Line Continuation**: Support trailing backslashes (`\`) or triple-quote blocks (`"""`) for pasting multi-line code or logs.
* **Double Ctrl+C Safety**: Press Ctrl+C once to cancel ongoing inputs; double-tap within 2s to exit cleanly.
* **Visual Diff Highlighting**: Instant syntax-colored diff cards (`+` green, `-` red, `@@` cyan) in `/diff` and during patch applications.
* **Kairos Status Cockpit**: Ambient HUD displaying current workspace, detected project build system, Sub-Cortex token surgery state, and active Kairos v1.0 engine.

### 5. Multi-Backend Inference & Zero-Config Auto-Detection
Kronumos auto-detects running local Ollama engines or environment API keys (`OPENAI_API_KEY`, `GROQ_API_KEY`) on first launch, providing zero-config setup out of the box:

```bash
# Cloudflare Workers AI ($0 edge serverless inference)
kronumos --backend cloudflare --cf-url https://kronumos-gateway.<account>.workers.dev

# Local Ollama GGUF (100% offline, zero API costs)
kronumos --backend ollama --ollama-model hf.co/NadevA23/Kronumos-GGUF:Q4_K_M

# OpenAI-compatible API (Groq, Together, vLLM, DeepSeek)
kronumos --backend openai --openai-url https://api.groq.com/openai/v1 --openai-key $GROQ_API_KEY --openai-model qwen-2.5-coder-32b
```

### 6. Persistent Configuration File
Avoid re-typing CLI flags by setting your preferred backend and options in `~/.config/kronumos/config.toml` (global) or `.kronumos.toml` (project-level):

```toml
# ~/.config/kronumos/config.toml or .kronumos.toml
backend = "ollama"
ollama_model = "hf.co/NadevA23/Kronumos-GGUF:Q4_K_M"
timeout = 120
max_iterations = 10
auto_rollback = true
```


## 🛠️ Built-in Agent Tools

During autonomous diagnosis, Kronumos invokes the following sub-cortex tools with zero human intervention:

| Tool | Purpose |
| :--- | :--- |
| `run_command` | Executes test runners, build commands, and compiler checks with timeout guards |
| `view_file` | Inspects exact source code lines and context |
| `search_code` | Searches codebase for symbol definitions or error text patterns across all project files |
| `list_files` | Explores repository file hierarchy and directory structure |
| `write_file` | Creates new files or writes full file content with automatic parent directory creation |
| `apply_patch` | Applies surgical, character-exact search-and-replace AST patches |
| `git_action` | Inspects diffs, manages branches, and commits verified fixes |


## ⌨️ Built-in Agent Slash Commands & Keyboard Shortcuts

| Command | Action |
| :--- | :--- |
| `Any text` | Freeform conversation — ask questions about errors, explain code, or request refactors |
| `@<path>` | Autocompletes via Tab and inlines workspace file content into model context |
| `!<cmd>` | Direct shell execution on physical hardware without LLM latency or token waste |
| `/fix` | Triggers the autonomous test-driven remediation loop |
| `/undo` | Reverts uncommitted patches immediately (guarantees zero dirty diff) |
| `/diff` | Displays the current uncommitted git diff in the workspace |
| `/test` | Executes project tests directly and scrubs framework noise with Sub-Cortex |
| `/stats` | Displays FinOps telemetry: pruned lines, session duration, and tokens saved |
| `/clear` | Clears conversation context buffer |
| `/help` | Displays command reference and agent capabilities |
| `/exit` | Exits the session cleanly (or double Ctrl+C) |


## 🛡️ Sub-Cortex Security Invariants & Critical File Guard

- **Zero-Leak Redaction**: All user inputs and command outputs pass through Tokenectomy's compiled ReDoS-safe linear regex engine. JWTs, Bearer tokens, private keys, and connection strings are automatically masked before prompt transmission.
- **Strict Sandbox & Path Traversal Guard**: Prevents path traversal (`../`) outside workspace boundaries. Prohibits reading or modifying sensitive credentials (`.env*`, `id_rsa*`, `.ssh/`, `.aws/`, `.gnupg/`, `passwd`, `.git/config`, `access_token`, `auth.json`).
- **Human-in-the-Loop Confirmation Gate**: Whenever the agent attempts to inspect or modify critical build manifests (`Cargo.toml`, `package.json`, `pyproject.toml`, `go.mod`, `Makefile`, `Dockerfile`, `.github/workflows/*`, `migrations/*`), it requires explicit terminal confirmation:
  - For viewing: `Allow agent to view this file? [Y/n]`
  - For patching / writing: `Allow this modification? [y/N/v (view proposed changes)]` with an interactive preview before applying changes.
- **Surgical Atomic Patches**: All code modifications are character-exact search-and-replace hunks. Kronumos never blindly rewrites entire source files.
- **Context Sliding Window**: Automatically compacts multi-turn debugging steps to prevent token overflow during long-running sessions.
