#!/bin/bash
set -e

echo "=== 1. Installing Ollama ==="
curl -fsSL https://ollama.com/install.sh | sh

echo "=== 2. Configuring SSH Authorization Key ==="
mkdir -p /root/.ollama ~/.ollama
cat << 'EOF' > ~/.ollama/id_ed25519
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtz
c2gtZWQyNTUxOQAAACAmGsq0A1RzE48r2I555m3uqeD/UI/fs1NLlJ4lX/SwqAAA
AIgCnmiIAp5oiAAAAAtzc2gtZWQyNTUxOQAAACAmGsq0A1RzE48r2I555m3uqeD/
UI/fs1NLlJ4lX/SwqAAAAECiwaALc4jQ9ChffZoU1bp5lHmJqjgOtQjT5OOmY34x
vyYayrQDVHMTjyvYjnnmbe6p4P9Qj9+zU0uUniVf9LCoAAAAAAECAwQF
-----END OPENSSH PRIVATE KEY-----
EOF
chmod 600 ~/.ollama/id_ed25519
cp -f ~/.ollama/id_ed25519 /root/.ollama/id_ed25519 2>/dev/null || true

cat << 'EOF' > ~/.ollama/id_ed25519.pub
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAICYayrQDVHMTjyvYjnnmbe6p4P9Qj9+zU0uUniVf9LCo
EOF
cp -f ~/.ollama/id_ed25519.pub /root/.ollama/id_ed25519.pub 2>/dev/null || true

echo "=== 3. Starting Ollama Service ==="
nohup ollama serve > /tmp/ollama.log 2>&1 &
sleep 5

echo "=== 4. Creating Modelfile ==="
cat << 'EOF' > Modelfile
FROM hf.co/mradermacher/Kronumos-i1-GGUF:Q4_K_M
TEMPLATE """{{ if .System }}<|im_start|>system
{{ .System }}<|im_end|>
{{ end }}{{ if .Prompt }}<|im_start|>user
{{ .Prompt }}<|im_end|>
{{ end }}<|im_start|>assistant
{{ .Response }}<|im_end|>
"""
PARAMETER stop "<|im_start|>"
PARAMETER stop "<|im_end|>"
PARAMETER temperature 0.2
PARAMETER top_p 0.95
SYSTEM """You are Kronumos, an autonomous software-repair and program repair agent. You analyze runtime failures, diagnose root causes, and produce verified unified diffs."""
EOF

echo "=== 5. Building Kronumos on Ollama ==="
ollama create -f Modelfile kronumos/Kronumos-2-kairos

echo "=== 6. Pushing to Ollama Hub ==="
ollama push kronumos/Kronumos-2-kairos

echo "=== ALL DONE! Model is LIVE at ollama.com/kronumos/Kronumos-2-kairos ==="
