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
          timestamp: new Date().toISOString(),
        }, null, 2),
        {
          headers: {
            "Content-Type": "application/json",
            ...CORS_HEADERS,
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
            ...CORS_HEADERS,
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

      // Optional Bearer Authentication check
      if (env.KRONUMOS_API_KEY) {
        const authHeader = request.headers.get("Authorization") || "";
        const expected = `Bearer ${env.KRONUMOS_API_KEY.trim()}`;
        if (authHeader.trim() !== expected) {
          return new Response(
            JSON.stringify({ error: "Unauthorized: Invalid or missing Bearer token" }),
            { status: 401, headers: { "Content-Type": "application/json", ...CORS_HEADERS } }
          );
        }
      }

      let body;
      try {
        body = await request.json();
      } catch (err) {
        return new Response(
          JSON.stringify({ error: "Invalid JSON payload" }),
          { status: 400, headers: { "Content-Type": "application/json", ...CORS_HEADERS } }
        );
      }

      const messages = body.messages || [];
      if (!Array.isArray(messages) || messages.length === 0) {
        return new Response(
          JSON.stringify({ error: "Missing or empty 'messages' array" }),
          { status: 400, headers: { "Content-Type": "application/json", ...CORS_HEADERS } }
        );
      }

      // Default model: Qwen 2.5 Coder 32B on Cloudflare Workers AI
      const model = body.model || env.DEFAULT_MODEL || "@cf/qwen/qwen2.5-coder-32b-instruct";
      const isStream = body.stream !== false; // Default to streaming

      try {
        const aiResponse = await env.AI.run(model, {
          messages: messages.map(m => ({
            role: m.role,
            content: m.content,
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
              ...CORS_HEADERS,
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
              ...CORS_HEADERS,
            },
          });
        }
      } catch (aiErr) {
        return new Response(
          JSON.stringify({
            error: "Workers AI execution error",
            details: aiErr.message || String(aiErr),
          }),
          { status: 500, headers: { "Content-Type": "application/json", ...CORS_HEADERS } }
        );
      }
    }

    return new Response("Not found", { status: 404, headers: CORS_HEADERS });
  },
};
