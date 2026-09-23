# ⚡ Kronumos Cloudflare Edge Gateway

Serverless, zero-operational-cost AI edge inference gateway for **Kronumos CLI** and autonomous agents, powered by **Cloudflare Workers AI**.

---

## 🌟 Why Cloudflare Workers AI for Kronumos?

- **$0 Operational Cost**: Free tier provides **10,000 Neurons per day** (~500+ debugging turns/day for free).
- **Sub-Second Global Edge Latency**: Direct GPU inference across Cloudflare's 300+ global datacenters.
- **Model**: Runs `@cf/qwen/qwen2.5-coder-32b-instruct` (or `@cf/meta/llama-3.1-8b-instruct-fast`).
- **Streaming**: Native Server-Sent Events (SSE) streaming with zero latency buffering.

---

## 🚀 60-Second Deployment

### 1. Install Wrangler & Log In
```bash
npm install -g wrangler
wrangler login
```

### 2. Test Locally
```bash
cd gateway
npm run dev
```
Open `http://localhost:8787/health` to verify:
```json
{
  "status": "online",
  "service": "Kronumos Cloudflare Edge Gateway",
  "version": "1.0.0",
  "runtime": "Cloudflare Workers AI",
  "default_model": "@cf/qwen/qwen2.5-coder-32b-instruct"
}
```

### 3. Deploy to the Edge ($0 Cloud)
```bash
npm run deploy
```
Wrangler will output your live URL:
```text
Published kronumos-gateway (1.23 sec)
  https://kronumos-gateway.<your-account>.workers.dev
```

### 4. (Optional) Set an API Secret for Private Testing
If you want to protect your gateway with a private key before public distribution:
```bash
npx wrangler secret put KRONUMOS_API_KEY
# Enter your secret password/key when prompted
```

---

## 💻 Connecting Kronumos CLI to the Gateway

Pass the URL to the CLI or export the environment variable:

```bash
# Via CLI argument:
kronumos --backend cloudflare --cf-url https://kronumos-gateway.<your-account>.workers.dev

# Or permanently in ~/.bashrc or ~/.zshrc:
export KRONUMOS_CF_URL="https://kronumos-gateway.<your-account>.workers.dev"
export KRONUMOS_CF_KEY="your-secret-if-set"

# Now simply run:
kronumos
```
