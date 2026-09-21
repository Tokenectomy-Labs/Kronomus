use axum::{
    extract::{Query, State},
    response::Html,
};
use crate::db::Database;
use crate::models::FilterQuery;
use crate::ui::{components::home_view, layout::base_layout};

pub async fn home_page(
    State(db): State<Database>,
    Query(params): Query<FilterQuery>,
) -> Html<String> {
    let tools = db
        .list_tools(params.q, params.category, params.chain)
        .unwrap_or_default();

    let categories = vec![
        "Smart Contract Security",
        "EVM RPC & Explorer",
        "Solana Ecosystem",
        "DeFi & DEX",
        "Oracles & Infrastructure",
        "Decentralized Storage",
        "Wallets & Governance",
        "Indexing & Subgraphs",
        "Zero-Knowledge & Privacy",
    ];

    let chains = vec![
        "Ethereum",
        "Solana",
        "Arbitrum",
        "Base",
        "Polygon",
        "Optimism",
        "IPFS",
        "Arweave",
        "Multi-chain",
    ];

    let content = home_view(&tools, &categories, &chains);
    let full_html = base_layout("Web3 MCP Directory // Anonymous & Permissionless", content);

    Html(full_html.into_string())
}
