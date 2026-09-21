# Web3 MCP Directory // Anonymous & Permissionless

Direktori terbuka dan **100% anonim** untuk Model Context Protocol (MCP) servers & AI agent tools di ekosistem Web3 (Ethereum, EVM, Solana, DeFi, Smart Contract Auditing, Storage, ZK Proofs).

Dibangun **100% menggunakan Rust** untuk Backend maupun Frontend (Axum + Maud + SQLite), dengan filosofi cypherpunk murni: **Zero KYC, Zero OAuth (tanpa Google/GitHub), Zero Email, Zero Birokrasi Web2**.

---

## ⚡ Fitur Utama

1. **Full Anonim & Tanpa Birokrasi Web2**
   - Siapa saja bisa mendaftarkan server Web3 MCP baru secara instan tanpa perlu mendaftar akun, tanpa verifikasi email, dan tanpa approval berbelit.
   - Tidak ada cookie pelacak, tidak ada analytics invasif, tidak ada PII (Personally Identifiable Information).

2. **100% Rust Fullstack**
   - **Backend**: Axum 0.8 + Tokio (asynchronous, zero-cost abstractions, sub-millisecond latency).
   - **Frontend**: Maud (type-safe compile-time HTML rendering langsung dari Rust).
   - **Storage**: SQLite embedded (`rusqlite` bundled) — single self-contained binary (~5.6 MB), tanpa butuh dependensi eksternal.

3. **Tampilan Minimalis (No Distracting Accents)**
   - Desain utilitarian monokrom yang bersih, fokus pada data densitas tinggi dan keterbacaan kode.
   - Tanpa gradien ungu/neon yang berlebihan atau elemen AI slop visual.

4. **1-Click MCP Config Generator**
   - Format siap pakai untuk **Claude Desktop** (`claude_desktop_config.json`).
   - Format siap pakai untuk **Cursor & Windsurf** (`mcp.json`).
   - Perintah 1-klik untuk **Antigravity CLI** (`agy mcp add <slug> -- <cmd> <args>`).

5. **Machine-to-Machine (M2M) API untuk AI Agents**
   - Agent otonom (Claude, Cursor, Cline, Antigravity) dapat meng-query dan menambahkan tools langsung lewat HTTP REST API:
     - `GET /api/tools` — Daftar semua Web3 MCP tools (JSON).
     - `GET /api/tools?q=solana&category=DeFi` — Filter pencarian instan.
     - `GET /api/tools/:slug` — Metadata dan schema spesifik.
     - `POST /api/tools` — Submission anonim tanpa token/autentikasi.
     - `GET /api/export` — Ekspor seluruh direktori ke file JSON offline.

---

## 📦 Koleksi Web3 MCP Bawaan (Pre-Seeded)

Direktori ini sudah langsung dilengkapi dengan Web3 MCP servers terverifikasi:
- **Etherscan Explorer MCP**: ABI kontrak terverifikasi, riwayat tx, event logs, gas tracker.
- **Foundry Anvil MCP**: Local EVM sandbox manipulation, fork testing, cheatcodes.
- **Slither Static Auditor MCP**: Detektor kerentanan Solidity (reentrancy, access control).
- **Aderyn Rust Solidity Linter MCP**: AST parser dan static analyzer Solidity berbasis Rust dari Cyfrin.
- **Solana Helius Agent MCP**: Query akun Solana, DAS tokens, simulasi transaksi.
- **Uniswap & DefiLlama Liquidity MCP**: Routing DEX swaps, cadangan pool V2/V3, TVL, dan harga token.
- **Chainlink Oracles MCP**: Data feeds kripto/forex, AggregatorV3 interface, CCIP tracking.
- **IPFS & Pinata Storage MCP**: Pinning file terdesentralisasi, CID query, dan IPFS metadata.
- **Safe Multisig MCP**: Inspeksi Gnosis Safe, pending threshold transactions, simulasi eksekusi.
- **The Graph Subgraph MCP**: Query GraphQL ke subgraph terdesentralisasi.
- **Circom & SnarkJS ZK MCP**: Inspeksi circuit Zero-Knowledge (.circom), R1CS constraints, Groth16 proof verifier.
- **Arweave & Irys Storage MCP**: Penyimpanan permanen on-chain dan estimasi biaya permaweb.

---

## 🚀 Cara Menjalankan

### 1. Jalankan Langsung Binary Release
```bash
./target/release/web3-mcp-anon
```
Server akan aktif di: `http://localhost:3000`

### 2. Jalankan Mode Development
```bash
cargo run
```

### 3. Ganti Port (Opsional)
```bash
PORT=8080 ./target/release/web3-mcp-anon
```

---

## 📡 REST API Examples

### List Semua Tools
```bash
curl http://localhost:3000/api/tools
```

### Cari Tools (Filter)
```bash
curl "http://localhost:3000/api/tools?q=solana"
```

### Submit Tool Baru secara Anonim
```bash
curl -X POST http://localhost:3000/api/tools \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Biconomy Smart Account MCP",
    "description": "ERC-4337 Account Abstraction bundling and gasless paymaster tooling.",
    "category": "Wallets & Governance",
    "chains": "Ethereum, Arbitrum, Base",
    "command": "npx",
    "args": "-y @biconomy/mcp-server",
    "env_vars": "BICONOMY_API_KEY",
    "repo_url": "https://github.com/biconomy/biconomy-mcp",
    "docs_url": "https://docs.biconomy.io",
    "author_alias": "0xAnon"
  }'
```
