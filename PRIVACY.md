# Tokenectomy Labs — Privacy Policy & Zero-Retention Security Shield

Last Updated: September 2026

Tokenectomy Labs ("Tokenectomy", "we", "us", or "our") is committed to protecting the privacy, confidentiality, and security of developers and enterprises utilizing Kronumos. This Privacy Policy outlines our data handling practices, our Zero Code Retention architecture, and your rights.

## 1. Core Commitment: Zero Code Retention (ZCR)

We believe that code is proprietary intellectual property. Unlike legacy consumer AI tools:
1. Zero Persistent Logging: The Kronumos Cloudflare Edge Gateway does NOT store, log, archive, or write user prompts, code snippets, diffs, or repository contents to any database, file system, or persistent cloud storage.
2. In-Memory Ephemeral Routing: When you issue an inference query via the Cloudflare Edge Gateway, messages are processed purely in ephemeral RAM within Cloudflare Workers AI edge isolates and immediately flushed from memory once the response stream closes.
3. No Model Training on User Data: Tokenectomy Labs does not use customer source code, test traces, or prompts to train, fine-tune, or improve any public or shared foundation models.

## 2. Edge Defense & Secret Redaction

To prevent accidental leakage of sensitive credentials, Kronumos employs a dual-layer sanitization pipeline:
1. Client-Side Sanitization: Before leaving your machine, the Kronumos CLI runs `tokenectomy::redact_secrets` to scrub AWS keys, GitHub tokens, JWTs, API keys, and private SSH certificates.
2. Edge Gateway Sanitization: As defense-in-depth, the Cloudflare Edge Gateway applies an automatic pattern scrubber that replaces detected credentials with redact markers before forwarding payloads to Workers AI inference.

## 3. Data We Collect and Why

We operate on a data minimization principle. The only data processed by the Cloudflare Edge Gateway includes:
1. Cryptographic Client IP (`cf-connecting-ip`): Used strictly for edge rate limiting (sliding-window anti-hammering) and DDoS mitigation. Rate limiter counters are kept in volatile edge memory and automatically expire.
2. Request Metadata: Payload size and HTTP headers necessary to enforce security boundaries and CORS compatibility.
3. Account Identifiers (Pro/Enterprise Tiers): When using an optional API key (`X-Kronumos-Key` or `Authorization: Bearer`), the key is checked to verify subscription tier entitlements.

## 4. Local-First & Air-Gapped Modes

For absolute confidentiality:
1. Ollama Offline Mode: Running `kronumos --backend ollama` executes inference 100% locally on your own GPU/CPU without transmitting a single byte over the Internet.
2. Local Configuration: All CLI settings, command history, and custom presets reside exclusively on your local workstation in `~/.config/kronumos/`.

## 5. Third-Party Service Providers

When using the default Cloudflare Edge Gateway, network traffic traverses Cloudflare Workers AI infrastructure governed by Cloudflare's security standards (SOC 2 Type II, ISO 27001, and GDPR compliance).

## 6. Enterprise Data Sovereignty & Custom Deployments

Enterprise organizations subject to strict regulatory frameworks (including HIPAA, SOC 2, and PCI-DSS) may license self-hosted, air-gapped deployments of Kronumos and Tokenectomy-Ultra within their private VPC or Kubernetes cluster with zero external egress.

For privacy questions or data protection officer inquiries:
- Contact: privacy@tokenectomy.com / security@tokenectomy.com
- Organization: Tokenectomy Labs
