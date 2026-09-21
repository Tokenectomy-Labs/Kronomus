use maud::{html, Markup};
use crate::models::McpTool;

pub fn home_view(
    tools: &[McpTool],
    categories: &[&str],
    chains: &[&str],
    pricing_models: &[&str],
) -> Markup {
    html! {
        div class="container" {
            section class="hero" {
                h1 { "Decentralized Web3 MCP Directory & Marketplace" }
                p {
                    "Pusat listing & jual-beli Model Context Protocol (MCP) servers untuk Web3 agents. 100% anonim, non-custodial, tanpa rekening bank, tanpa Stripe KYC, dan tanpa birokrasi Web2. Pembayaran langsung peer-to-peer antar wallet kripto."
                }
            }

            section class="controls" {
                div class="search-row" {
                    input 
                        type="text" 
                        id="searchInput" 
                        class="search-input" 
                        placeholder="Cari Web3 MCP tools, chain, fitur, atau model monetisasi..." 
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
                    select id="pricingFilter" class="filter-select" onchange="filterTools()" {
                        option value="All" { "All Monetization" }
                        @for pr in pricing_models {
                            option value=(pr) { (pr) }
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

    let is_paid = tool.pricing_model != "Free & Open Source";

    html! {
        div 
            class="card"
            data-name=(tool.name)
            data-desc=(tool.description)
            data-cat=(tool.category)
            data-chains=(chains_joined)
            data-pricing=(tool.pricing_model)
        {
            div {
                div class="card-header" {
                    div {
                        h2 class="card-title" { (tool.name) }
                        div class="card-meta" {
                            @if is_paid {
                                span class="tag tag-paid" { (tool.price) }
                                span class="tag" { (tool.pricing_model) }
                            } @else {
                                span class="tag tag-free" { (tool.price) }
                            }
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
                        "CREATOR: " (tool.author_alias)
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

                @if let Some(payout) = &tool.payout_address {
                    button 
                        class="btn-action btn-pay" 
                        onclick=(format!("openPaymentModal('{}', '{}', '{}', '{}')", 
                            tool.name.replace('\'', "\\'"),
                            tool.pricing_model.replace('\'', "\\'"),
                            tool.price.replace('\'', "\\'"),
                            payout.replace('\'', "\\'")
                        )) 
                    {
                        @if is_paid {
                            "Direct Pay ⚡"
                        } @else {
                            "Tip Creator ⚡"
                        }
                    }
                }

                @if let Some(comm) = &tool.commercial_url {
                    a href=(comm) target="_blank" rel="noopener noreferrer" class="btn-action btn-buy" {
                        "Marketplace / Buy ↗"
                    }
                }

                button 
                    class="btn-action" 
                    onclick=(format!("copyText(this, '{}')", full_cmd.replace('\'', "\\'"))) 
                {
                    "Copy Cmd"
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
