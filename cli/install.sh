#!/usr/bin/env bash
# ⚡ Kronumos CLI Installer
# Installs the Kronumos Autonomous Bug Remediation & SRE Agent

set -e

echo ""
echo "                                       /▀▀\/▀▀\\"
echo "                                     ▄██████ (O)"
echo "                            \\ /    /████████\\_/ \\"
echo "                             \\____████████████/  \\"
echo "                                    \\█████████    \\"
echo "                                      ▀████████    \\"
echo "                                        ████████    |"
echo "                                 ▄████▄  ███████    /"
echo "                              ▄█████████▄ █████    /"
echo "                           ▄████▀▀   ▀▀███████   _/"
echo "                           ▀████▄▄▄▄▄▄████▀▀  ~-~"
echo ""
echo "    ██╗  ██╗██████╗  ██████╗ ███╗   ██╗██╗   ██╗███╗   ███╗ ██████╗ ███████╗"
echo "    ██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██║   ██║████╗ ████║██╔═══██╗██╔════╝"
echo "    █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║   ██║██╔████╔██║██║   ██║███████╗"
echo "    ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██║╚██╔╝██║██║   ██║╚════██║"
echo "    ██║  ██╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝███████║"
echo "    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚══════╝"
echo ""
echo "                 Autonomous Code Remediation & SRE Agent • v1.0"
echo ""

INSTALL_DIR="${CARGO_HOME:-$HOME/.cargo}/bin"
mkdir -p "$INSTALL_DIR"

if command -v cargo >/dev/null 2>&1; then
    echo "⚡ Building Kronumos from official repository via Cargo..."
    if cargo install --git https://github.com/Tokenectomy-Labs/Tokenectomy --bin kronumos --force 2>/dev/null; then
        echo "✅ Kronumos successfully installed to $INSTALL_DIR/kronumos"
    else
        echo "⚡ Retrying with latest active release branch..."
        cargo install --git https://github.com/Tokenectomy-Labs/Tokenectomy --branch fix/scorecard-gold-remediation --bin kronumos --force
        echo "✅ Kronumos successfully installed to $INSTALL_DIR/kronumos"
    fi
else
    echo "❌ Cargo not found. Please install Rust toolchain (curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh) or download pre-compiled releases from GitHub Releases."
    exit 1
fi

if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo ""
    echo "⚠️ Notice: $INSTALL_DIR is not in your PATH."
    echo "  Add this to your shell config (~/.bashrc or ~/.zshrc):"
    echo "  export PATH=\"\$HOME/.cargo/bin:\$PATH\""
fi

echo ""
echo "🚀 Quickstart:"
echo "  1. Run with local Ollama:    kronumos --backend ollama"
echo "  2. Run with Cloudflare Edge: kronumos --backend cloudflare --cf-url <your-worker-url>"
echo "  3. Autonomous fix mode:      kronumos --fix"
echo ""
