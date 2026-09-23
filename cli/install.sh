#!/usr/bin/env bash
# ⚡ Kronumos CLI Installer
# Installs the Kronumos Autonomous Bug Remediation & SRE Agent

set -e

echo ""
echo "  ╦╔═╦═╗╔═╗╔╗╔╦ ╦╔╦╗╔═╗╔═╗"
echo "  ╠╩╗╠╦╝║ ║║║║║ ║║║║║ ║╚═╗"
echo "  ╩ ╩╩╚═╚═╝╝╚╝╚═╝╩ ╩╚═╝╚═╝"
echo "  Autonomous Code Remediation & SRE Agent • v1.0"
echo ""

INSTALL_DIR="${HOME}/.cargo/bin"
mkdir -p "$INSTALL_DIR"

if command -v cargo >/dev/null 2>&1; then
    echo "⚡ Building Kronumos from official repository via Cargo..."
    cargo install --git https://github.com/Tokenectomy-Labs/Tokenectomy --bin kronumos --force
    echo ""
    echo "✅ Kronumos successfully installed to $INSTALL_DIR/kronumos"
else
    echo "❌ Cargo not found. Please install Rust from https://rustup.rs or download pre-compiled releases."
    exit 1
fi

echo ""
echo "🚀 Quickstart:"
echo "  1. Run with local Ollama:    kronumos --backend ollama"
echo "  2. Run with Cloudflare Edge: kronumos --backend cloudflare --cf-url <your-worker-url>"
echo "  3. Autonomous fix mode:      kronumos --fix"
echo ""
