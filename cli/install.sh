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
    SHA_URL="${BINARY_URL}.sha256"
    TEMP_FILE="$(mktemp)"
    TEMP_SHA="$(mktemp)"

    if curl -fsSL "$BINARY_URL" -o "$TEMP_FILE" 2>/dev/null; then
        # Cryptographic Integrity Verification
        if curl -fsSL "$SHA_URL" -o "$TEMP_SHA" 2>/dev/null; then
            EXPECTED_SHA="$(cat "$TEMP_SHA" | tr -d '[:space:]')"
            ACTUAL_SHA=""
            if command -v sha256sum >/dev/null 2>&1; then
                ACTUAL_SHA="$(sha256sum "$TEMP_FILE" | awk '{print $1}')"
            elif command -v shasum >/dev/null 2>&1; then
                ACTUAL_SHA="$(shasum -a 256 "$TEMP_FILE" | awk '{print $1}')"
            fi
            if [ -n "$EXPECTED_SHA" ] && [ -n "$ACTUAL_SHA" ]; then
                if [ "$EXPECTED_SHA" != "$ACTUAL_SHA" ]; then
                    echo "❌ Security Error: SHA256 checksum verification failed!"
                    echo "   Expected: $EXPECTED_SHA"
                    echo "   Actual:   $ACTUAL_SHA"
                    rm -f "$TEMP_FILE" "$TEMP_SHA"
                    exit 1
                fi
                echo "🔒 SHA256 cryptographic integrity verified."
            fi
            rm -f "$TEMP_SHA"
        fi

        chmod +x "$TEMP_FILE"
        mv "$TEMP_FILE" "$INSTALL_DIR/kronumos"
        echo "✅ Kronumos successfully installed to $INSTALL_DIR/kronumos"
    else
        rm -f "$TEMP_FILE" "$TEMP_SHA"
        # If GitHub release asset is not yet uploaded, use already installed binary or notify
        if [ -f "$INSTALL_DIR/kronumos" ]; then
            echo "✅ Kronumos is already installed at $INSTALL_DIR/kronumos"
        else
            echo "❌ Failed to download pre-compiled release binary from $BINARY_URL."
            if [ "$OS" = "darwin" ]; then
                echo "💡 macOS Notice: Standalone Darwin binaries are rolling out. If you have Rust/Cargo installed, you can build from source, or run Kronumos in Linux Docker container:"
                echo "   docker run -it --rm -v \$(pwd):/workspace ghcr.io/tokenectomy-labs/kronumos:latest"
            fi
            echo "   Please check https://github.com/Tokenectomy-Labs/Kronomus/releases for available platform artifacts."
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
echo "  1. Start interactive REPL:   kronumos"
echo "  2. Autonomous fix mode:      kronumos --fix"
echo "  3. Run with local Ollama:    kronumos --backend ollama"
echo ""
