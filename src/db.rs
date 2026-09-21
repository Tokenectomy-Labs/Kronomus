use std::fs;
use std::path::Path;
use std::sync::{Arc, Mutex};
use rusqlite::{params, Connection, Result};
use uuid::Uuid;
use chrono::Utc;
use crate::models::{McpTool, SubmitToolRequest};

#[derive(Clone)]
pub struct Database {
    conn: Arc<Mutex<Connection>>,
}

impl Database {
    pub fn init() -> Result<Self> {
        let db_dir = Path::new("./data");
        if !db_dir.exists() {
            fs::create_dir_all(db_dir).map_err(|e| {
                rusqlite::Error::ToSqlConversionFailure(Box::new(e))
            })?;
        }

        let conn = Connection::open("./data/mcp.db")?;
        
        conn.execute(
            "CREATE TABLE IF NOT EXISTS tools (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE,
                description TEXT NOT NULL,
                category TEXT NOT NULL,
                chains TEXT NOT NULL,
                transport TEXT NOT NULL,
                command TEXT NOT NULL,
                args TEXT NOT NULL,
                env_vars TEXT NOT NULL,
                config_snippet TEXT NOT NULL,
                repo_url TEXT NOT NULL,
                docs_url TEXT,
                author_alias TEXT NOT NULL,
                pricing_model TEXT NOT NULL DEFAULT 'Free & Open Source',
                price TEXT NOT NULL DEFAULT 'Free',
                payout_address TEXT,
                commercial_url TEXT,
                verified INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL
            )",
            [],
        )?;

        // Ensure columns exist for backwards-compatibility migration
        let _ = conn.execute("ALTER TABLE tools ADD COLUMN pricing_model TEXT NOT NULL DEFAULT 'Free & Open Source'", []);
        let _ = conn.execute("ALTER TABLE tools ADD COLUMN price TEXT NOT NULL DEFAULT 'Free'", []);
        let _ = conn.execute("ALTER TABLE tools ADD COLUMN payout_address TEXT", []);
        let _ = conn.execute("ALTER TABLE tools ADD COLUMN commercial_url TEXT", []);

        let db = Database {
            conn: Arc::new(Mutex::new(conn)),
        };

        db.seed_if_empty()?;

        Ok(db)
    }

    fn seed_if_empty(&self) -> Result<()> {
        let conn = self.conn.lock().unwrap();
        let count: i64 = conn.query_row("SELECT COUNT(*) FROM tools", [], |r| r.get(0))?;
        if count > 0 {
            return Ok(());
        }

        let seeds = vec![
            (
                "Etherscan Explorer MCP",
                "etherscan-mcp",
                "Inspect verified contract ABIs, source code, event logs, token balances, and EVM gas prices directly from Etherscan and L2 explorers.",
                "EVM RPC & Explorer",
                "Ethereum, Arbitrum, Optimism, Base, Polygon",
                "stdio",
                "npx",
                "-y @modelcontextprotocol/server-etherscan",
                "ETHERSCAN_API_KEY",
                "https://github.com/modelcontextprotocol/servers/tree/main/src/etherscan",
                Some("https://etherscan.io/apis"),
                "0xCypherpunk",
                "Free & Open Source",
                "Free (Tips Welcome)",
                Some("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"),
                None,
                1
            ),
            (
                "Foundry Anvil MCP",
                "foundry-anvil-mcp",
                "Run and manipulate a local EVM sandbox. Supports fork tests, trace decodes, state dumps, cheatcodes, and transaction simulation.",
                "Smart Contract Security",
                "Ethereum, EVM compatible",
                "stdio",
                "anvil-mcp",
                "--port 8545 --fork-url https://eth.llamarpc.com",
                "RPC_URL",
                "https://github.com/foundry-rs/foundry",
                Some("https://book.getfoundry.sh/anvil/"),
                "paradigm_anon",
                "Free & Open Source",
                "Free",
                Some("0x000000000000000000000000000000000000dEaD"),
                None,
                1
            ),
            (
                "Slither Static Auditor Pro MCP",
                "slither-auditor-mcp",
                "Crytic's Solidity static analysis framework exposing AST inspection, vulnerability detection (reentrancy, uninitialized state, unchecked calls).",
                "Smart Contract Security",
                "Ethereum, EVM",
                "stdio",
                "slither-mcp",
                "--ast-mode --json-report",
                "SLITHER_PATH",
                "https://github.com/crytic/slither",
                Some("https://github.com/crytic/slither/wiki"),
                "trail_of_anon",
                "Crypto License",
                "0.08 ETH (One-Time)",
                Some("0x71C25e3692604Fa7F876aD67364b63e8F45aF98C"),
                Some("https://t.me/anon_auditor_bot"),
                1
            ),
            (
                "Aderyn Rust Solidity Linter MCP",
                "aderyn-mcp",
                "Cyfrin's Rust-native static code analyzer for Solidity. Instant AST parsing, cyclomatic complexity metrics, and vulnerability reporting.",
                "Smart Contract Security",
                "Ethereum, Arbitrum, Base",
                "stdio",
                "aderyn-mcp",
                "--output report.json",
                "",
                "https://github.com/Cyfrin/aderyn",
                Some("https://cyfrin.io/aderyn"),
                "cyfrin_ghost",
                "Free & Open Source",
                "Free",
                Some("0x3a4bC8174fD378D8a56E9D7A5a8C7d27e28A6133"),
                None,
                1
            ),
            (
                "Solana Helius Agent MCP",
                "solana-helius-mcp",
                "Query Solana account state, parse DAS (Digital Asset Standard) tokens, resolve SNS domains, and simulate Solana transaction payloads.",
                "Solana Ecosystem",
                "Solana",
                "stdio",
                "npx",
                "-y helius-mcp-server",
                "HELIUS_API_KEY",
                "https://github.com/helius-labs/helius-mcp",
                Some("https://docs.helius.dev/"),
                "sol_anon",
                "Pay-per-Call (x402)",
                "0.001 SOL / 1k requests",
                Some("Helius7gA3KkHNxv2qQfXbVn8KjLp9X7Vn8KjLp9X7V"),
                Some("https://helius.dev/pricing"),
                1
            ),
            (
                "Uniswap & DefiLlama Liquidity MCP",
                "uniswap-defillama-mcp",
                "Access decentralized exchange swap routing, V2/V3 liquidity pool reserves, TVL statistics, token prices, and historical yield data.",
                "DeFi & DEX",
                "Ethereum, Arbitrum, Base, Polygon, Optimism",
                "stdio",
                "npx",
                "-y @defillama/mcp-server",
                "",
                "https://github.com/DefiLlama/defillama-mcp",
                Some("https://defillama.com/docs/api"),
                "0xDeFiDegens",
                "Tipping / Donation",
                "Any crypto donation",
                Some("0x084694b4e3FB9E59590937F505174F3298546454"),
                None,
                1
            ),
            (
                "Flashloan Arbitrage Hunter MCP",
                "flashloan-arbitrage-mcp",
                "Automated multi-DEX price discrepancy scanner with Aave V3 / Balancer flashloan execution simulation without upfront capital.",
                "DeFi & DEX",
                "Ethereum, Arbitrum, Base",
                "stdio",
                "arb-hunter-mcp",
                "--network arbitrum --min-profit 0.02eth",
                "PRIVATE_KEY,RPC_URL",
                "https://github.com/anon-web3/flashloan-arb-mcp",
                Some("https://github.com/anon-web3/flashloan-arb-mcp#readme"),
                "0xDarkPoolAnon",
                "Crypto License",
                "0.25 ETH (Lifetime Key)",
                Some("0x9E75d9e5a8C7d27e28A61333a4bC8174fD378D8a"),
                Some("https://t.me/darkpool_anon"),
                1
            ),
            (
                "Chainlink Oracles & Data Feeds MCP",
                "chainlink-oracles-mcp",
                "Retrieve round data, heartbeat timestamps, decimals, and AggregatorV3Interface feeds for crypto, forex, commodities, and CCIP statuses.",
                "Oracles & Infrastructure",
                "Ethereum, Avalanche, Polygon, Arbitrum",
                "stdio",
                "npx",
                "-y chainlink-mcp-server",
                "CHAINLINK_RPC_URL",
                "https://github.com/smartcontractkit/chainlink",
                Some("https://docs.chain.link/data-feeds"),
                "link_marine_anon",
                "Free & Open Source",
                "Free",
                Some("0x514910771AF9Ca656af840dff83E8264EcF986CA"),
                None,
                1
            ),
            (
                "IPFS & Pinata Storage MCP",
                "ipfs-pinata-mcp",
                "Decentralized content-addressed file storage. Pin files, query CIDs, navigate DAG nodes, and manage IPFS metadata for smart contracts.",
                "Decentralized Storage",
                "IPFS, Filecoin",
                "stdio",
                "npx",
                "-y pinata-mcp-server",
                "PINATA_JWT",
                "https://github.com/PinataCloud/pinata-mcp",
                Some("https://docs.pinata.cloud/"),
                "ipfs_seed",
                "Pay-per-Call (x402)",
                "$5 USDC / 10 GB",
                Some("0x1111111254fb6c44bac0bed2854e76f90643097d"),
                Some("https://pinata.cloud"),
                1
            ),
            (
                "Safe Multisig & Keystore MCP",
                "safe-multisig-mcp",
                "Inspect Gnosis Safe multisig configurations, read pending multi-owner transaction proposals, verify threshold signatures, and simulate executions.",
                "Wallets & Governance",
                "Ethereum, Polygon, Arbitrum, Optimism, Base",
                "stdio",
                "safe-mcp-server",
                "--network mainnet",
                "SAFE_API_KEY",
                "https://github.com/safe-global/safe-core-sdk",
                Some("https://docs.safe.global/"),
                "safe_keeper",
                "Tipping / Donation",
                "Tips Welcome",
                Some("0x8B3192f5eE8D277e269153549646b5aF63d6b1d4"),
                None,
                1
            ),
            (
                "The Graph Subgraph Query MCP",
                "the-graph-mcp",
                "Query decentralized indexing subgraphs via GraphQL. Fetch processed blockchain entities, transfers, balances, and governance votes.",
                "Indexing & Subgraphs",
                "Ethereum, Arbitrum, Multi-chain",
                "stdio",
                "npx",
                "-y @graphprotocol/mcp-server",
                "GRAPH_API_KEY",
                "https://github.com/graphprotocol/graph-node",
                Some("https://thegraph.com/docs/"),
                "subgraph_indexer",
                "Free & Open Source",
                "Free",
                Some("0xc944E90C64B2c07662A292be6244BDf05Cda44a7"),
                None,
                1
            ),
            (
                "Circom & SnarkJS ZK Prover MCP",
                "circom-snarkjs-mcp",
                "Inspect Zero-Knowledge arithmetic circuits (.circom), verify witness generation, check constraint counts (R1CS), and validate Groth16 proofs.",
                "Zero-Knowledge & Privacy",
                "Ethereum, Circom, Noir",
                "stdio",
                "snarkjs-mcp",
                "--r1cs-info",
                "",
                "https://github.com/iden3/snarkjs",
                Some("https://docs.circom.io/"),
                "zk_ghost_99",
                "Pay-per-Call (x402)",
                "0.005 ETH / 50 proofs",
                Some("0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97"),
                Some("https://docs.circom.io/"),
                1
            ),
            (
                "Arweave & Irys Permanent Storage MCP",
                "arweave-irys-mcp",
                "Permanent on-chain storage tooling. Upload immutable dApp states, metadata, and audit logs with one-time payment fee estimation.",
                "Decentralized Storage",
                "Arweave, Multi-chain",
                "stdio",
                "npx",
                "-y @irys/mcp-server",
                "IRYS_PRIVATE_KEY",
                "https://github.com/Irys-xyz/mcp-server",
                Some("https://docs.irys.xyz/"),
                "permaweb_anon",
                "Tipping / Donation",
                "Permaweb Tips",
                Some("0x00000000219ab540356cbb839cbe05303d7705fa"),
                None,
                1
            )
        ];

        for s in seeds {
            let id = Uuid::new_v4().to_string();
            let args_vec: Vec<String> = s.7.split_whitespace().map(|x| x.to_string()).collect();
            let env_vec: Vec<String> = if s.8.is_empty() {
                vec![]
            } else {
                s.8.split(',').map(|x| x.trim().to_string()).collect()
            };

            let config_json = serde_json::json!({
                "mcpServers": {
                    s.1: {
                        "command": s.6,
                        "args": args_vec,
                        "env": env_vec.iter().map(|k| (k.clone(), serde_json::Value::String(format!("<YOUR_{}>", k)))).collect::<serde_json::Map<String, serde_json::Value>>()
                    }
                }
            });

            let now = Utc::now().to_rfc3339();

            conn.execute(
                "INSERT INTO tools (
                    id, name, slug, description, category, chains, transport,
                    command, args, env_vars, config_snippet, repo_url, docs_url,
                    author_alias, pricing_model, price, payout_address, commercial_url,
                    verified, created_at
                ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16, ?17, ?18, ?19, ?20)",
                params![
                    id,
                    s.0,
                    s.1,
                    s.2,
                    s.3,
                    s.4,
                    s.5,
                    s.6,
                    s.7,
                    s.8,
                    serde_json::to_string_pretty(&config_json).unwrap_or_default(),
                    s.9,
                    s.10,
                    s.11,
                    s.12,
                    s.13,
                    s.14,
                    s.15,
                    s.16,
                    now
                ],
            )?;
        }

        Ok(())
    }

    pub fn list_tools(&self, q: Option<String>, category: Option<String>, chain: Option<String>, pricing: Option<String>) -> Result<Vec<McpTool>> {
        let conn = self.conn.lock().unwrap();
        let mut sql = String::from("SELECT id, name, slug, description, category, chains, transport, command, args, env_vars, config_snippet, repo_url, docs_url, author_alias, pricing_model, price, payout_address, commercial_url, verified, created_at FROM tools WHERE 1=1");
        
        let mut params_vec: Vec<Box<dyn rusqlite::ToSql>> = Vec::new();

        if let Some(cat) = category {
            if !cat.is_empty() && cat != "All" {
                sql.push_str(" AND category = ?");
                params_vec.push(Box::new(cat));
            }
        }

        if let Some(ch) = chain {
            if !ch.is_empty() && ch != "All" {
                sql.push_str(" AND chains LIKE ?");
                params_vec.push(Box::new(format!("%{}%", ch)));
            }
        }

        if let Some(pr) = pricing {
            if !pr.is_empty() && pr != "All" {
                sql.push_str(" AND pricing_model = ?");
                params_vec.push(Box::new(pr));
            }
        }

        if let Some(query) = q {
            let trimmed = query.trim().to_lowercase();
            if !trimmed.is_empty() {
                sql.push_str(" AND (LOWER(name) LIKE ? OR LOWER(description) LIKE ? OR LOWER(chains) LIKE ? OR LOWER(category) LIKE ? OR LOWER(pricing_model) LIKE ?)");
                let pattern = format!("%{}%", trimmed);
                params_vec.push(Box::new(pattern.clone()));
                params_vec.push(Box::new(pattern.clone()));
                params_vec.push(Box::new(pattern.clone()));
                params_vec.push(Box::new(pattern.clone()));
                params_vec.push(Box::new(pattern));
            }
        }

        sql.push_str(" ORDER BY verified DESC, created_at DESC");

        let mut stmt = conn.prepare(&sql)?;
        
        let params_slice: Vec<&dyn rusqlite::ToSql> = params_vec.iter().map(|b| b.as_ref()).collect();
        let rows = stmt.query_map(params_slice.as_slice(), |row| {
            let chains_str: String = row.get(5)?;
            let args_str: String = row.get(8)?;
            let env_str: String = row.get(9)?;
            let verified_int: i32 = row.get(18)?;

            Ok(McpTool {
                id: row.get(0)?,
                name: row.get(1)?,
                slug: row.get(2)?,
                description: row.get(3)?,
                category: row.get(4)?,
                chains: chains_str.split(',').map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect(),
                transport: row.get(6)?,
                command: row.get(7)?,
                args: args_str.split_whitespace().map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect(),
                env_vars: env_str.split(',').map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect(),
                config_snippet: row.get(10)?,
                repo_url: row.get(11)?,
                docs_url: row.get(12)?,
                author_alias: row.get(13)?,
                pricing_model: row.get(14)?,
                price: row.get(15)?,
                payout_address: row.get(16)?,
                commercial_url: row.get(17)?,
                verified: verified_int == 1,
                created_at: row.get(19)?,
            })
        })?;

        let mut tools = Vec::new();
        for r in rows {
            tools.push(r?);
        }

        Ok(tools)
    }

    pub fn get_by_slug(&self, slug: &str) -> Result<Option<McpTool>> {
        let conn = self.conn.lock().unwrap();
        let mut stmt = conn.prepare("SELECT id, name, slug, description, category, chains, transport, command, args, env_vars, config_snippet, repo_url, docs_url, author_alias, pricing_model, price, payout_address, commercial_url, verified, created_at FROM tools WHERE slug = ?1")?;
        
        let mut rows = stmt.query_map([slug], |row| {
            let chains_str: String = row.get(5)?;
            let args_str: String = row.get(8)?;
            let env_str: String = row.get(9)?;
            let verified_int: i32 = row.get(18)?;

            Ok(McpTool {
                id: row.get(0)?,
                name: row.get(1)?,
                slug: row.get(2)?,
                description: row.get(3)?,
                category: row.get(4)?,
                chains: chains_str.split(',').map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect(),
                transport: row.get(6)?,
                command: row.get(7)?,
                args: args_str.split_whitespace().map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect(),
                env_vars: env_str.split(',').map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect(),
                config_snippet: row.get(10)?,
                repo_url: row.get(11)?,
                docs_url: row.get(12)?,
                author_alias: row.get(13)?,
                pricing_model: row.get(14)?,
                price: row.get(15)?,
                payout_address: row.get(16)?,
                commercial_url: row.get(17)?,
                verified: verified_int == 1,
                created_at: row.get(19)?,
            })
        })?;

        if let Some(res) = rows.next() {
            Ok(Some(res?))
        } else {
            Ok(None)
        }
    }

    pub fn insert_tool(&self, req: SubmitToolRequest) -> Result<McpTool> {
        let id = Uuid::new_v4().to_string();
        let base_slug = req.name
            .to_lowercase()
            .chars()
            .map(|c| if c.is_alphanumeric() { c } else { '-' })
            .collect::<String>()
            .trim_matches('-')
            .to_string();
        
        // ensure uniqueness
        let slug = format!("{}-{}", base_slug, &id[..6]);

        let transport = req.transport.unwrap_or_else(|| "stdio".to_string());
        let args_str = req.args.unwrap_or_default();
        let env_str = req.env_vars.unwrap_or_default();
        let author_alias = req.author_alias
            .filter(|a| !a.trim().is_empty())
            .unwrap_or_else(|| "0xAnon".to_string());
        let pricing_model = req.pricing_model
            .filter(|p| !p.trim().is_empty())
            .unwrap_or_else(|| "Free & Open Source".to_string());
        let price = req.price
            .filter(|p| !p.trim().is_empty())
            .unwrap_or_else(|| "Free".to_string());

        let args_vec: Vec<String> = args_str.split_whitespace().map(|s| s.to_string()).collect();
        let env_vec: Vec<String> = env_str.split(',').map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect();

        let config_json = serde_json::json!({
            "mcpServers": {
                &slug: {
                    "command": req.command,
                    "args": args_vec,
                    "env": env_vec.iter().map(|k| (k.clone(), serde_json::Value::String(format!("<YOUR_{}>", k)))).collect::<serde_json::Map<String, serde_json::Value>>()
                }
            }
        });
        let config_snippet = serde_json::to_string_pretty(&config_json).unwrap_or_default();

        let now = Utc::now().to_rfc3339();

        let conn = self.conn.lock().unwrap();
        conn.execute(
            "INSERT INTO tools (
                id, name, slug, description, category, chains, transport,
                command, args, env_vars, config_snippet, repo_url, docs_url,
                author_alias, pricing_model, price, payout_address, commercial_url,
                verified, created_at
            ) VALUES (?1, ?2, ?3, ?4, ?5, ?6, ?7, ?8, ?9, ?10, ?11, ?12, ?13, ?14, ?15, ?16, ?17, ?18, ?19, ?20)",
            params![
                id,
                req.name,
                slug,
                req.description,
                req.category,
                req.chains,
                transport,
                req.command,
                args_str,
                env_str,
                config_snippet,
                req.repo_url,
                req.docs_url,
                author_alias,
                pricing_model,
                price,
                req.payout_address,
                req.commercial_url,
                0, // community anonymous submitted
                now
            ],
        )?;

        Ok(McpTool {
            id,
            name: req.name,
            slug,
            description: req.description,
            category: req.category,
            chains: req.chains.split(',').map(|s| s.trim().to_string()).filter(|s| !s.is_empty()).collect(),
            transport,
            command: req.command,
            args: args_vec,
            env_vars: env_vec,
            config_snippet,
            repo_url: req.repo_url,
            docs_url: req.docs_url,
            author_alias,
            pricing_model,
            price,
            payout_address: req.payout_address,
            commercial_url: req.commercial_url,
            verified: false,
            created_at: now,
        })
    }
}
