/**
 * ⚡ Kronumos Cloudflare Edge Gateway
 * ===================================
 * Serverless, zero-cost AI edge inference gateway for Kronumos CLI and agents.
 * 
 * Powered by Cloudflare Workers AI:
 * - Free Tier: 10,000 Neurons/day (~500+ debugging turns/day for $0)
 * - Supported models:
 *     - @cf/qwen/qwen2.5-coder-32b-instruct (default: elite code reasoning)
 *     - @cf/meta/llama-3.1-8b-instruct-fast (ultra-low latency fallback)
 * - Protocols: Server-Sent Events (SSE) streaming & JSON
 */

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Kronumos-Key",
};

const SECURITY_HEADERS = {
  ...CORS_HEADERS,
  "X-Content-Type-Options": "nosniff",
  "X-Frame-Options": "DENY",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
};

// Edge-level Secret & Credential Scrubber (Defense-in-Depth for Enterprise / Zero-Leakage)
function redactEdgeSecrets(text) {
  if (typeof text !== "string") return text;
  return text
    .replace(/(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,255}/g, "[REDACTED_GITHUB_TOKEN]")
    .replace(/AKIA[0-9A-Z]{16}/g, "[REDACTED_AWS_KEY]")
    .replace(/eyJ[A-Za-z0-9-_]{10,}\.[A-Za-z0-9-_]{10,}\.[A-Za-z0-9-_]{10,}/g, "[REDACTED_JWT]")
    .replace(/(?:sk-[A-Za-z0-9]{20,}|sk-ant-[A-Za-z0-9-_]{20,})/g, "[REDACTED_API_KEY]")
    .replace(/-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (?:RSA |EC |OPENSSH )?PRIVATE KEY-----/g, "[REDACTED_PRIVATE_KEY]");
}

// ── In-Memory Edge Rate Limiter & Security Shields ─────────────────────────
const ipRateLimits = new Map();
const ipBurstLimits = new Map();

const RATE_LIMIT_WINDOW_MS = 60 * 60 * 1000; // 1 hour sliding window
const BURST_LIMIT_WINDOW_MS = 10 * 1000;      // 10 seconds sliding window
const MAX_BURST_PER_10S = 6;                  // Max 6 requests per 10s

function checkRateLimit(ip, maxRequests, windowMs = RATE_LIMIT_WINDOW_MS) {
  const now = Date.now();

  // Periodic garbage collection if map exceeds 5000 entries
  if (ipRateLimits.size > 5000) {
    for (const [key, data] of ipRateLimits.entries()) {
      if (now > data.resetAt) ipRateLimits.delete(key);
    }
  }

  let record = ipRateLimits.get(ip);
  if (!record || now > record.resetAt) {
    record = { count: 1, resetAt: now + windowMs };
    ipRateLimits.set(ip, record);
    return { allowed: true, remaining: maxRequests - 1, resetAt: record.resetAt };
  }

  if (record.count >= maxRequests) {
    return { allowed: false, remaining: 0, resetAt: record.resetAt };
  }

  record.count += 1;
  return { allowed: true, remaining: maxRequests - record.count, resetAt: record.resetAt };
}

function checkBurstLimit(ip, maxBurst = MAX_BURST_PER_10S, windowMs = BURST_LIMIT_WINDOW_MS) {
  const now = Date.now();

  if (ipBurstLimits.size > 5000) {
    for (const [key, data] of ipBurstLimits.entries()) {
      if (now > data.resetAt) ipBurstLimits.delete(key);
    }
  }

  let record = ipBurstLimits.get(ip);
  if (!record || now > record.resetAt) {
    record = { count: 1, resetAt: now + windowMs };
    ipBurstLimits.set(ip, record);
    return { allowed: true };
  }

  if (record.count >= maxBurst) {
    return { allowed: false, retryAfter: Math.max(1, Math.ceil((record.resetAt - now) / 1000)) };
  }

  record.count += 1;
  return { allowed: true };
}

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    // Health check endpoint
    if (url.pathname === "/health" || (url.pathname === "/" && request.method === "GET")) {
      return new Response(
        JSON.stringify({
          status: "online",
          service: "Kronumos Cloudflare Edge Gateway",
          version: "1.0.0",
          runtime: "Cloudflare Workers AI",
          default_model: "@cf/qwen/qwen2.5-coder-32b-instruct",
          rate_limit_per_hour: env.RATE_LIMIT_PER_HOUR || "30",
          timestamp: new Date().toISOString(),
        }, null, 2),
        {
          headers: {
            "Content-Type": "application/json",
            ...SECURITY_HEADERS,
          },
        }
      );
    }

    // Models list endpoint (OpenAI SDK / Cursor / Continue compatibility)
    if (url.pathname === "/models" || url.pathname === "/v1/models") {
      return new Response(
        JSON.stringify({
          object: "list",
          data: [
            {
              id: "@cf/qwen/qwen2.5-coder-32b-instruct",
              object: "model",
              created: 1700000000,
              owned_by: "cloudflare",
            },
            {
              id: "kronumos",
              object: "model",
              created: 1700000000,
              owned_by: "tokenectomy-labs",
            },
            {
              id: "@cf/meta/llama-3.1-8b-instruct-fast",
              object: "model",
              created: 1700000000,
              owned_by: "cloudflare",
            }
          ],
        }, null, 2),
        {
          headers: {
            "Content-Type": "application/json",
            ...SECURITY_HEADERS,
          },
        }
      );
    }

    // Chat completion / Streaming inference endpoint
    if (
      url.pathname === "/chat" ||
      url.pathname === "/v1/chat/completions" ||
      url.pathname === "/chat/completions" ||
      (url.pathname === "/" && request.method === "POST")
    ) {
      if (request.method !== "POST") {
        return new Response("Method not allowed", { status: 405, headers: CORS_HEADERS });
      }

      // Security Shield 1: Payload Size Guard (max 128KB to prevent memory exhaustion)
      const contentLength = parseInt(request.headers.get("content-length") || "0", 10);
      if (contentLength > 131072) {
        return new Response(
          JSON.stringify({
            error: "Payload Too Large",
            message_en: "Request body exceeds maximum allowed limit of 128KB.",
            message_id: "Ukuran permintaan melebihi batas maksimum 128KB."
          }, null, 2),
          { status: 413, headers: { "Content-Type": "application/json", ...SECURITY_HEADERS } }
        );
      }

      // Security Shield 2: Cryptographically Trusted Client IP (prevents spoofing via X-Forwarded-For)
      const clientIp = request.headers.get("cf-connecting-ip") || "anonymous";

      // Auth / Tier Check: Pro / VIP API Key bypass or IP-based Rate Limiter for free users
      const authHeader = request.headers.get("Authorization") || "";
      const customKeyHeader = request.headers.get("X-Kronumos-Key") || "";
      const clientKey = (authHeader.startsWith("Bearer ") ? authHeader.substring(7) : customKeyHeader).trim();
      
      const isAuthorizedVip = (env.KRONUMOS_API_KEY && clientKey === env.KRONUMOS_API_KEY.trim()) ||
                              (env.PRO_KEYS && env.PRO_KEYS.split(",").map(k => k.trim()).includes(clientKey));

      let rateLimitHeaders = {};
      if (!isAuthorizedVip) {
        // Security Shield 3: Anti-Hammering / DDoS Burst Limiter (max 6 req / 10s)
        const burstStatus = checkBurstLimit(clientIp);
        if (!burstStatus.allowed) {
          return new Response(
            JSON.stringify({
              error: "Too Many Requests (Burst limit)",
              message_en: "Too many rapid requests. Please wait a few seconds before trying again.",
              message_id: "Terlalu banyak permintaan dalam waktu singkat. Harap tunggu beberapa detik sebelum mencoba lagi."
            }, null, 2),
            {
              status: 429,
              headers: {
                "Content-Type": "application/json",
                "Retry-After": String(burstStatus.retryAfter || 2),
                ...SECURITY_HEADERS,
              }
            }
          );
        }

        // Security Shield 4: Hourly Sliding-Window Rate Limiter
        const maxRequests = parseInt(env.RATE_LIMIT_PER_HOUR || "30", 10);
        const limitStatus = checkRateLimit(clientIp, maxRequests);

        rateLimitHeaders = {
          "X-RateLimit-Limit": String(maxRequests),
          "X-RateLimit-Remaining": String(limitStatus.remaining),
          "X-RateLimit-Reset": String(Math.ceil(limitStatus.resetAt / 1000)),
        };

        if (!limitStatus.allowed) {
          return new Response(
            JSON.stringify({
              error: "Rate limit exceeded (Free Cloudflare Tier)",
              message_en: `Free tier limit reached (${maxRequests} requests/hour per IP). Use local Ollama ('kronumos --backend ollama') for unlimited requests, or wait until the next hour.`,
              message_id: `Batas kuota gratis tercapai (${maxRequests} request/jam per IP). Gunakan Ollama lokal ('kronumos --backend ollama') untuk pemakaian tanpa batas, atau tunggu hingga periode berikutnya.`,
              reset_at: new Date(limitStatus.resetAt).toISOString(),
            }, null, 2),
            {
              status: 429,
              headers: {
                "Content-Type": "application/json",
                "Retry-After": String(Math.max(1, Math.ceil((limitStatus.resetAt - Date.now()) / 1000))),
                ...SECURITY_HEADERS,
                ...rateLimitHeaders,
              }
            }
          );
        }
      }

      let body;
      try {
        body = await request.json();
      } catch (err) {
        return new Response(
          JSON.stringify({
            error: "Invalid JSON payload",
            message_en: "Failed to parse JSON body.",
            message_id: "Gagal memproses JSON payload."
          }, null, 2),
          { status: 400, headers: { "Content-Type": "application/json", ...SECURITY_HEADERS } }
        );
      }

      const messages = body.messages || [];
      if (!Array.isArray(messages) || messages.length === 0) {
        return new Response(
          JSON.stringify({
            error: "Missing or empty 'messages' array",
            message_en: "The 'messages' array is required and must not be empty.",
            message_id: "Array 'messages' wajib diisi dan tidak boleh kosong."
          }, null, 2),
          { status: 400, headers: { "Content-Type": "application/json", ...SECURITY_HEADERS } }
        );
      }

      // Security Shield 5: Message array length and item size validation
      if (messages.length > 50) {
        return new Response(
          JSON.stringify({
            error: "Too many messages in history",
            message_en: "Conversation history exceeds maximum limit of 50 messages.",
            message_id: "Riwayat percakapan melebihi batas maksimum 50 pesan."
          }, null, 2),
          { status: 400, headers: { "Content-Type": "application/json", ...SECURITY_HEADERS } }
        );
      }

      for (const m of messages) {
        if (typeof m.content === "string" && m.content.length > 25000) {
          return new Response(
            JSON.stringify({
              error: "Message too large",
              message_en: "Single message content exceeds maximum limit of 25,000 characters.",
              message_id: "Isi pesan melebihi batas maksimum 25.000 karakter."
            }, null, 2),
            { status: 400, headers: { "Content-Type": "application/json", ...SECURITY_HEADERS } }
          );
        }
      }

      // Identity & Language Invariant: Ensure the model knows its true creator and language
      const processedMessages = [...messages];
      const IDENTITY_INVARIANT = `\n\n[Core Identity & Creator Invariant (MANDATORY):
- Your name is Kronumos Kairos.
- Creator: Tokenectomy Labs.
- Engine: Tokenectomy Rust Sub-Cortex.
- FORBIDDEN ENTITIES: You must NEVER claim to be created by Anthropic, OpenAI, Meta, Google, or any other company.
- Response when asked in English: "I was created and engineered by Tokenectomy Labs." (Strictly 100% English, no Indonesian words).
- Response when asked in Indonesian: "Saya dibuat dan dikembangkan oleh Tokenectomy Labs."
- Language Mirroring: Always mirror the user's language with 100% precision. If the user writes in English, reply in English. If the user writes in Indonesian, reply in Indonesian.]`;

      if (processedMessages.length > 0 && processedMessages[0].role === "system") {
        if (!processedMessages[0].content.includes("Core Identity & Creator Invariant")) {
          processedMessages[0] = {
            ...processedMessages[0],
            content: processedMessages[0].content + IDENTITY_INVARIANT,
          };
        }
      } else {
        processedMessages.unshift({
          role: "system",
          content: "You are Kronumos Kairos, an elite developer assistant, autonomous bug remediation engineer, and SRE copilot." + IDENTITY_INVARIANT,
        });
      }

      // Default model: Qwen 2.5 Coder 32B on Cloudflare Workers AI
      const model = body.model || env.DEFAULT_MODEL || "@cf/qwen/qwen2.5-coder-32b-instruct";
      const isStream = body.stream !== false; // Default to streaming

      try {
        const aiResponse = await env.AI.run(model, {
          messages: processedMessages.map(m => ({
            role: m.role,
            content: redactEdgeSecrets(m.content),
          })),
          stream: isStream,
          max_tokens: body.max_tokens || 1024,
          temperature: body.temperature || 0.2,
        });

        if (isStream) {
          // Return SSE stream directly to CLI client
          return new Response(aiResponse, {
            headers: {
              "Content-Type": "text/event-stream; charset=utf-8",
              "Cache-Control": "no-cache",
              "Connection": "keep-alive",
              ...SECURITY_HEADERS,
              ...rateLimitHeaders,
            },
          });
        } else {
          const respText = typeof aiResponse === "string" ? aiResponse : (aiResponse.response || JSON.stringify(aiResponse));
          const responsePayload = {
            id: `chatcmpl-${Date.now()}`,
            object: "chat.completion",
            created: Math.floor(Date.now() / 1000),
            model: model,
            response: respText,
            choices: [
              {
                index: 0,
                message: {
                  role: "assistant",
                  content: respText,
                },
                finish_reason: "stop",
              }
            ],
            usage: {
              prompt_tokens: 0,
              completion_tokens: 0,
              total_tokens: 0,
            }
          };
          return new Response(JSON.stringify(responsePayload), {
            headers: {
              "Content-Type": "application/json",
              ...SECURITY_HEADERS,
              ...rateLimitHeaders,
            },
          });
        }
      } catch (aiErr) {
        return new Response(
          JSON.stringify({
            error: "Workers AI execution error",
            details: aiErr.message || String(aiErr),
          }),
          { status: 500, headers: { "Content-Type": "application/json", ...SECURITY_HEADERS } }
        );
      }
    }

    return new Response("Not found", { status: 404, headers: SECURITY_HEADERS });
  },
};
