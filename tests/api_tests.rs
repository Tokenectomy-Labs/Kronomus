use std::sync::Arc;
use rusqlite::Connection;

#[test]
fn test_database_seed_and_query() {
    let conn = Connection::open_in_memory().unwrap();
    conn.execute(
        "CREATE TABLE tools (
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
            verified INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL
        )",
        [],
    ).unwrap();

    conn.execute(
        "INSERT INTO tools VALUES (
            'id-1', 'Etherscan MCP', 'etherscan-mcp', 'Ethereum explorer tools',
            'EVM RPC & Explorer', 'Ethereum, Arbitrum', 'stdio', 'npx', '-y etherscan',
            'ETHERSCAN_KEY', '{}', 'https://github.com/org/repo', NULL, '0xAnon', 1, '2026-09-21T00:00:00Z'
        )",
        [],
    ).unwrap();

    let count: i64 = conn.query_row("SELECT COUNT(*) FROM tools", [], |r| r.get(0)).unwrap();
    assert_eq!(count, 1);
}
