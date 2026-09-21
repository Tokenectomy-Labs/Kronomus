use maud::{html, Markup};
use crate::models::McpTool;

pub fn home_view(tools: &[McpTool], categories: &[&str], chains: &[&str]) -> Markup {
    html! {
        div class="container" {
            section class="hero" {
                h1 { "Decentralized Web3 MCP Directory" }
                p {
                    "Curated and community-submitted Model Context Protocol (MCP) servers for Web3 agents. Zero accounts, zero KYC, zero bureaucracy. Ready to copy for Claude, Cursor, and Antigravity."
                }
            }

            section class="controls" {
                div class="search-row" {
                    input 
                        type="text" 
                        id="searchInput" 
                        class="search-input" 
                        placeholder="Search Web3 MCP servers by keyword, protocol, chain, or capability..." 
                        oninput="filterTools()";
                }
                div class="filter-row" {
                    select id="categoryFilter" class="filter-select" onchange="filterTools()" {
                        option value="All" { "All Categories" }
                        @for cat in categories {
                            option value=(cat) { (cat) }
                        }
                    }
                    select id="chainFilter" class="filter-select" onchange="filterTools()" {
                        option value="All" { "All Chains" }
                        @for chain in chains {
                            option value=(chain) { (chain) }
                        }
                    }
                    span id="toolCount" class="counter" {
                        (tools.len()) " tools listed"
                    }
                }
            }

            section class="grid" {
                @for tool in tools {
                    (tool_card(tool))
                }
            }
        }
    }
}

pub fn tool_card(tool: &McpTool) -> Markup {
    let args_joined = tool.args.join(" ");
    let env_joined = tool.env_vars.join(",");
    let chains_joined = tool.chains.join(", ");
    let full_cmd = if args_joined.is_empty() {
        tool.command.clone()
    } else {
        format!("{} {}", tool.command, args_joined)
    };

    html! {
        div 
            class="card"
            data-name=(tool.name)
            data-desc=(tool.description)
            data-cat=(tool.category)
            data-chains=(chains_joined)
        {
            div {
                div class="card-header" {
                    div {
                        h2 class="card-title" { (tool.name) }
                        div class="card-meta" {
                            @if tool.verified {
                                span class="tag tag-verified" { "Verified" }
                            } @else {
                                span class="tag" { "Community" }
                            }
                            span class="tag" { (tool.category) }
                            @for chain in &tool.chains {
                                span class="tag" { (chain) }
                            }
                        }
                    }
                }
                p class="card-desc" style="margin-top: 12px;" {
                    (tool.description)
                }
            }

            div {
                div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;" {
                    span style="font-size: 11px; font-family: var(--mono-font); color: var(--text-dim);" {
                        "TRANSPORT: " (tool.transport.to_uppercase())
                    }
                    span style="font-size: 11px; font-family: var(--mono-font); color: var(--text-dim);" {
                        "BY: " (tool.author_alias)
                    }
                }
                div class="code-box" {
                    (full_cmd)
                }
            }

            div class="card-actions" {
                button 
                    class="btn-action" 
                    onclick=(format!("openConfigModal('{}', '{}', '{}', '{}', '{}')", 
                        tool.name.replace('\'', "\\'"), 
                        tool.command.replace('\'', "\\'"), 
                        args_joined.replace('\'', "\\'"), 
                        env_joined.replace('\'', "\\'"), 
                        tool.slug
                    )) 
                {
                    "MCP Config"
                }

                button 
                    class="btn-action" 
                    onclick=(format!("copyText(this, '{}')", full_cmd.replace('\'', "\\'"))) 
                {
                    "Copy Command"
                }

                a href=(tool.repo_url) target="_blank" rel="noopener noreferrer" class="btn-action" {
                    "Repo ↗"
                }

                @if let Some(docs) = &tool.docs_url {
                    a href=(docs) target="_blank" rel="noopener noreferrer" class="btn-action" {
                        "Docs ↗"
                    }
                }
            }
        }
    }
}
