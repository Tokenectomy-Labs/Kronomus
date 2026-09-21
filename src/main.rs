mod models;
mod db;
mod ui;
mod handlers;

use std::net::SocketAddr;
use std::env;
use axum::{
    routing::{get, post},
    Router,
};
use tower_http::cors::{Any, CorsLayer};
use tracing_subscriber::{layer::SubscriberExt, util::SubscriberInitExt};

use crate::db::Database;
use crate::handlers::{api, views};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    tracing_subscriber::registry()
        .with(
            tracing_subscriber::EnvFilter::try_from_default_env()
                .unwrap_or_else(|_| "web3_mcp_anon=info,tower_http=info".into()),
        )
        .with(tracing_subscriber::fmt::layer())
        .init();

    tracing::info!("Initializing SQLite database for Web3 MCP Directory...");
    let db = Database::init()?;

    let cors = CorsLayer::new()
        .allow_origin(Any)
        .allow_methods(Any)
        .allow_headers(Any);

    let app = Router::new()
        .route("/", get(views::home_page))
        .route("/api/tools", get(api::get_tools))
        .route("/api/tools/{slug}", get(api::get_tool_by_slug))
        .route("/api/submit", post(api::submit_tool))
        .route("/api/tools", post(api::submit_tool))
        .route("/api/export", get(api::export_tools))
        .layer(cors)
        .with_state(db);

    let port: u16 = env::var("PORT")
        .ok()
        .and_then(|p| p.parse().ok())
        .unwrap_or(3000);

    let addr = SocketAddr::from(([0, 0, 0, 0], port));
    tracing::info!("Anonymous Web3 MCP Directory running on http://{}", addr);

    let listener = tokio::net::TcpListener::bind(addr).await?;
    axum::serve(listener, app).await?;

    Ok(())
}
