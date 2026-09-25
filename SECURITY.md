# Tokenectomy Labs — Security Policy & Coordinated Vulnerability Disclosure

Security is fundamental to Tokenectomy Labs. We engineer autonomous developer tools designed to heal software while safeguarding system integrity and confidentiality.

## 1. Supported Versions

Security updates and critical patches are actively provided for the following releases:

| Version | Supported | Gateway Status |
| :--- | :--- | :--- |
| v1.0.x | Yes | Active (Edge Workers AI) |
| Development (main) | Yes | Rolling Canary |

## 2. Reporting a Security Vulnerability

If you discover a potential security vulnerability in Kronumos, the Cloudflare Edge Gateway, or the Tokenectomy Sub-Cortex, please report it responsibly.

DO NOT file public GitHub issues for security vulnerabilities.

Please report vulnerabilities directly via email to:
- Primary Security Desk: security@tokenectomy.com
- Security Lead: support@tokenectomy.com

Include the following information in your report:
1. Type of vulnerability (e.g. sandbox escape, path traversal, edge rate-limit bypass, prompt injection);
2. Clear step-by-step reproduction instructions or proof-of-concept (PoC);
3. Operating system, Kronumos version, and CLI flags used;
4. Potential impact or blast radius of the issue.

## 3. Vulnerability Response Timeline

Upon receiving a valid security disclosure:
- Initial Acknowledgment: Within 24 business hours.
- Triage & Severity Assessment: Within 48 hours.
- Patch Deployment: Critical security fixes are deployed to the Cloudflare Edge Gateway within 24 hours of triage and released as a hotfix CLI release within 72 hours.
- Coordinated Public Advisory: Published following verification and deployment of mitigations.

## 4. Security Architecture Highlights

Kronumos integrates multiple defense-in-depth layers:
1. Path Traversal & Workspace Isolation: `is_safe_workspace_path` prevents reading or modifying files outside the designated workspace.
2. Sensitive Credential Blacklisting: Automatic blocking of credential stores, SSH keys, `.env` files, `.aws/`, and keystores.
3. Dual-Layer Secret Redaction: Regex and entropy sanitization runs both client-side and server-side at the Edge Gateway.
4. Cryptographic Binary Integrity: Installer validates SHA256 checksums before binary execution.
5. In-Memory Ephemeral Edge: Zero persistent logging of user code or messages.
