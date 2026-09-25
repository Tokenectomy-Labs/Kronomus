#!/usr/bin/env bash
# ⚡ Kronumos CLI Installer
# Installs the Kronumos Autonomous Bug Remediation & SRE Agent

set -e

echo ""
echo "    ██╗  ██╗██████╗  ██████╗ ███╗   ██╗██╗   ██╗███╗   ███╗ ██████╗ ███████╗"
echo "    ██║ ██╔╝██╔══██╗██╔═══██╗████╗  ██║██║   ██║████╗ ████║██╔═══██╗██╔════╝"
echo "    █████╔╝ ██████╔╝██║   ██║██╔██╗ ██║██║   ██║██╔████╔██║██║   ██║███████╗"
echo "    ██╔═██╗ ██╔══██╗██║   ██║██║╚██╗██║██║   ██║██║╚██╔╝██║██║   ██║╚════██║"
echo "    ██║  ██╗██║  ██║╚██████╔╝██║ ╚████║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝███████║"
echo "    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝ ╚══════╝"
echo ""
echo "                     · K R O N U M O S   K A I R O S ·"
echo "               Autonomous Code Remediation & SRE Agent • v1.0"
echo ""

INSTALL_DIR="${CARGO_HOME:-$HOME/.cargo}/bin"
mkdir -p "$INSTALL_DIR"

# 1. Check if local private core exists for developer builds
if [ -d "$HOME/Tokenonmix/Kronumos-Core" ] && command -v cargo >/dev/null 2>&1; then
    echo "⚡ Found local Kronumos-Core, compiling release binary..."
    cargo install --path "$HOME/Tokenonmix/Kronumos-Core" --force
    echo "✅ Kronumos successfully installed to $INSTALL_DIR/kronumos"
else
    # 2. Fetch standalone release binary
    echo "⚡ Downloading Kronumos pre-compiled binary release..."
    OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
    ARCH="$(uname -m)"
    case "$ARCH" in
        x86_64) ARCH="amd64" ;;
        aarch64|arm64) ARCH="arm64" ;;
        *) echo "❌ Unsupported architecture: $ARCH"; exit 1 ;;
    esac

    BINARY_URL="https://github.com/Tokenectomy-Labs/Kronomus/releases/latest/download/kronumos-${OS}-${ARCH}"
    TEMP_FILE="$(mktemp)"
    if curl -fsSL "$BINARY_URL" -o "$TEMP_FILE" 2>/dev/null; then
        chmod +x "$TEMP_FILE"
        mv "$TEMP_FILE" "$INSTALL_DIR/kronumos"
        echo "✅ Kronumos successfully installed to $INSTALL_DIR/kronumos"
    else
        rm -f "$TEMP_FILE"
        # If GitHub release asset is not yet uploaded, use already installed binary or notify
        if [ -f "$INSTALL_DIR/kronumos" ]; then
            echo "✅ Kronumos is already installed at $INSTALL_DIR/kronumos"
        else
            echo "❌ Failed to download release binary from $BINARY_URL."
            echo "   Please check https://github.com/Tokenectomy-Labs/Kronomus/releases for latest artifacts."
            exit 1
        fi
    fi
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
