use axum::{
    extract::{Path, Query, State},
    http::StatusCode,
    response::IntoResponse,
    Json,
};
use crate::db::Database;
use crate::models::{FilterQuery, SubmitToolRequest};

pub async fn get_tools(
    State(db): State<Database>,
    Query(params): Query<FilterQuery>,
) -> impl IntoResponse {
    match db.list_tools(params.q, params.category, params.chain, params.pricing) {
        Ok(tools) => (StatusCode::OK, Json(tools)).into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

pub async fn get_tool_by_slug(
    State(db): State<Database>,
    Path(slug): Path<String>,
) -> impl IntoResponse {
    match db.get_by_slug(&slug) {
        Ok(Some(tool)) => (StatusCode::OK, Json(tool)).into_response(),
        Ok(None) => (StatusCode::NOT_FOUND, "Tool not found").into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

pub async fn submit_tool(
    State(db): State<Database>,
    Json(payload): Json<SubmitToolRequest>,
) -> impl IntoResponse {
    if payload.name.trim().is_empty() || payload.command.trim().is_empty() || payload.repo_url.trim().is_empty() {
        return (StatusCode::BAD_REQUEST, "Name, command, and repo_url are required").into_response();
    }

    match db.insert_tool(payload) {
        Ok(tool) => (StatusCode::CREATED, Json(tool)).into_response(),
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}

pub async fn export_tools(
    State(db): State<Database>,
) -> impl IntoResponse {
    match db.list_tools(None, None, None, None) {
        Ok(tools) => {
            let json_str = serde_json::to_string_pretty(&tools).unwrap_or_default();
            (
                StatusCode::OK,
                [
                    ("Content-Type", "application/json"),
                    ("Content-Disposition", "attachment; filename=\"web3-mcp-directory.json\""),
                ],
                json_str,
            ).into_response()
        }
        Err(e) => (StatusCode::INTERNAL_SERVER_ERROR, e.to_string()).into_response(),
    }
}
