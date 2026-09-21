use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct McpTool {
    pub id: String,
    pub name: String,
    pub slug: String,
    pub description: String,
    pub category: String,
    pub chains: Vec<String>,
    pub transport: String,
    pub command: String,
    pub args: Vec<String>,
    pub env_vars: Vec<String>,
    pub config_snippet: String,
    pub repo_url: String,
    pub docs_url: Option<String>,
    pub author_alias: String,
    pub verified: bool,
    pub created_at: String,
}

#[derive(Debug, Clone, Deserialize)]
pub struct SubmitToolRequest {
    pub name: String,
    pub description: String,
    pub category: String,
    pub chains: String, // comma separated or single
    pub transport: Option<String>,
    pub command: String,
    pub args: Option<String>, // space or comma separated
    pub env_vars: Option<String>,
    pub repo_url: String,
    pub docs_url: Option<String>,
    pub author_alias: Option<String>,
}

#[derive(Debug, Clone, Deserialize)]
pub struct FilterQuery {
    pub q: Option<String>,
    pub category: Option<String>,
    pub chain: Option<String>,
}
