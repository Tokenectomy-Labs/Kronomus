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

### 1. Interactive Chat REPL (Transparent Terminal)
Launch directly into the interactive agent loop:
```bash
kronumos
```

### 2. Autonomous Non-Interactive Fix Loop
Point Kronumos at a failing project, immediately run the test suite, plan a fix, apply surgical patches, and verify clean test passes:
```bash
kronumos --fix
```

### 3. Inference Backends
Kronumos supports multiple inference backends:

```bash
# Cloudflare Workers AI ($0 edge serverless inference)
kronumos --backend cloudflare --cf-url https://kronumos-gateway.<account>.workers.dev

# Local Ollama GGUF (100% offline, zero API costs)
kronumos --backend ollama --ollama-model hf.co/NadevA23/Kronumos-GGUF:Q4_K_M

# OpenAI-compatible API (Groq, Together, vLLM, DeepSeek)
kronumos --backend openai --openai-url https://api.groq.com/openai/v1 --openai-key $GROQ_API_KEY --openai-model qwen-2.5-coder-32b
```


## ⌨️ Built-in Agent Slash Commands

| Command | Action |
| :--- | :--- |
| `Any text` | Freeform conversation — ask questions about errors, explain code, or request refactors |
| `/fix` | Triggers the autonomous test-driven remediation loop |
| `/diff` | Displays the current uncommitted git diff in the workspace |
| `/test` | Executes project tests directly and scrubs framework noise with Sub-Cortex |
| `/clear` | Clears conversation context buffer |
| `/help` | Displays command reference and agent capabilities |
| `/exit` | Exits the session cleanly with a zero dirty diff guarantee |


## 🛡️ Sub-Cortex Security Invariant

- **Zero-Leak Redaction**: All user inputs and command outputs pass through Tokenectomy's compiled ReDoS-safe linear regex engine. JWTs, Bearer tokens, and connection strings are automatically masked before prompt transmission.
- **Surgical Atomic Patches**: All code modifications are character-exact search-and-replace hunks. Kronumos never blindly rewrites entire source files.
