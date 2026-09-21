use maud::{html, Markup, DOCTYPE};
use crate::ui::styles::CSS;

pub fn base_layout(title: &str, content: Markup) -> Markup {
    html! {
        (DOCTYPE)
        html lang="en" {
            head {
                meta charset="utf-8";
                meta name="viewport" content="width=device-width, initial-scale=1.0";
                title { (title) }
                meta name="description" content="Anonymous Web3 Model Context Protocol (MCP) Directory. Zero KYC, zero OAuth, pure permissionless listing.";
                style { (CSS) }
            }
            body {
                header {
                    div class="container header-inner" {
                        div class="brand" {
                            a href="/" class="brand-title" { "WEB3-MCP // ANONYMOUS" }
                            span class="badge-anon" { "ZERO-AUTH" }
                            span class="badge-anon" { "100% RUST" }
                        }
                        nav {
                            a href="/" { "Directory" }
                            a href="/api/tools" target="_blank" { "JSON API" }
                            a href="/api/export" download="web3-mcp-directory.json" { "Export" }
                            button class="btn-submit-nav" onclick="openSubmitModal()" { "+ Submit Tool" }
                        }
                    }
                }

                main {
                    (content)
                }

                footer {
                    div class="container footer-inner" {
                        div {
                            "Built with Rust (Axum + Maud + SQLite). Zero tracking, zero cookies, zero Web2 gatekeeping."
                        }
                        div {
                            "Status: Permissionless Registry // M2M Native"
                        }
                    }
                }

                // Global Submission Modal
                div id="submitModal" class="modal-overlay" style="display: none;" {
                    div class="modal-content" {
                        div class="modal-header" {
                            span class="modal-title" { "Submit Web3 MCP Server (Anonymous)" }
                            button class="btn-close" onclick="closeSubmitModal()" { "×" }
                        }
                        p style="font-size: 12px; color: var(--text-muted); margin-bottom: 16px;" {
                            "No email, no Google/GitHub OAuth, no KYC. Your tool will be indexed immediately for AI agents."
                        }
                        form id="submitForm" onsubmit="handleAnonymousSubmit(event)" {
                            div class="form-group" {
                                label class="form-label" { "Tool Name *" }
                                input type="text" name="name" required class="form-input" placeholder="e.g. Uniswap V4 Pool Inspector MCP";
                            }
                            div class="form-group" {
                                label class="form-label" { "Description *" }
                                textarea name="description" required rows="2" class="form-textarea" placeholder="Describe what capabilities this MCP server exposes to AI agents..." {}
                            }
                            div style="display: flex; gap: 10px;" {
                                div class="form-group" style="flex: 1;" {
                                    label class="form-label" { "Category *" }
                                    select name="category" required class="form-select" {
                                        option value="Smart Contract Security" { "Smart Contract Security" }
                                        option value="EVM RPC & Explorer" { "EVM RPC & Explorer" }
                                        option value="Solana Ecosystem" { "Solana Ecosystem" }
                                        option value="DeFi & DEX" { "DeFi & DEX" }
                                        option value="Oracles & Infrastructure" { "Oracles & Infrastructure" }
                                        option value="Decentralized Storage" { "Decentralized Storage" }
                                        option value="Wallets & Governance" { "Wallets & Governance" }
                                        option value="Indexing & Subgraphs" { "Indexing & Subgraphs" }
                                        option value="Zero-Knowledge & Privacy" { "Zero-Knowledge & Privacy" }
                                    }
                                }
                                div class="form-group" style="flex: 1;" {
                                    label class="form-label" { "Chains / Networks *" }
                                    input type="text" name="chains" required class="form-input" placeholder="e.g. Ethereum, Base, Solana";
                                }
                            }
                            div style="display: flex; gap: 10px;" {
                                div class="form-group" style="flex: 1;" {
                                    label class="form-label" { "Executable / Binary *" }
                                    input type="text" name="command" required class="form-input" placeholder="e.g. npx, docker, cargo, python";
                                }
                                div class="form-group" style="flex: 2;" {
                                    label class="form-label" { "Arguments" }
                                    input type="text" name="args" class="form-input" placeholder="e.g. -y @package/name --network mainnet";
                                }
                            }
                            div class="form-group" {
                                label class="form-label" { "Required Env Vars (comma separated)" }
                                input type="text" name="env_vars" class="form-input" placeholder="e.g. ALCHEMY_KEY, PRIVATE_KEY";
                            }
                            div style="display: flex; gap: 10px;" {
                                div class="form-group" style="flex: 1;" {
                                    label class="form-label" { "Repository URL *" }
                                    input type="url" name="repo_url" required class="form-input" placeholder="https://github.com/org/repo";
                                }
                                div class="form-group" style="flex: 1;" {
                                    label class="form-label" { "Documentation URL" }
                                    input type="url" name="docs_url" class="form-input" placeholder="https://docs.example.com";
                                }
                            }
                            div class="form-group" {
                                label class="form-label" { "Author Alias (Optional - Default: 0xAnon)" }
                                input type="text" name="author_alias" class="form-input" placeholder="0xAnon / your.eth / pseudonym";
                            }
                            button type="submit" id="btnSubmitForm" class="btn-primary" {
                                "Submit Tool Anonymously"
                            }
                            div id="submitResult" style="margin-top: 10px; font-family: var(--mono-font); font-size: 12px; display: none;" {}
                        }
                    }
                }

                // Global Config Inspector Modal
                div id="configModal" class="modal-overlay" style="display: none;" {
                    div class="modal-content" {
                        div class="modal-header" {
                            span id="configModalTitle" class="modal-title" { "MCP Configuration" }
                            button class="btn-close" onclick="closeConfigModal()" { "×" }
                        }
                        div style="display: flex; gap: 8px; margin-bottom: 12px;" {
                            button class="btn-action active" id="tabClaude" onclick="switchConfigTab('claude')" { "Claude Desktop" }
                            button class="btn-action" id="tabCursor" onclick="switchConfigTab('cursor')" { "Cursor / Windsurf" }
                            button class="btn-action" id="tabAgy" onclick="switchConfigTab('agy')" { "Antigravity CLI" }
                        }
                        pre id="configModalBody" class="code-box" style="padding: 14px; max-height: 360px; overflow: auto; white-space: pre;" {}
                        div style="margin-top: 14px; display: flex; justify-content: flex-end; gap: 8px;" {
                            button class="btn-action" id="btnCopyModal" onclick="copyCurrentModalConfig()" { "Copy to Clipboard" }
                            button class="btn-action" onclick="closeConfigModal()" { "Close" }
                        }
                    }
                }

                script {
                    (maud::PreEscaped(r#"
                    let activeToolData = null;
                    let currentTab = 'claude';

                    function filterTools() {
                        const q = document.getElementById('searchInput').value.toLowerCase().trim();
                        const cat = document.getElementById('categoryFilter').value;
                        const chain = document.getElementById('chainFilter').value;
                        const cards = document.querySelectorAll('.card');
                        let visibleCount = 0;

                        cards.forEach(card => {
                            const name = card.getAttribute('data-name').toLowerCase();
                            const desc = card.getAttribute('data-desc').toLowerCase();
                            const cardCat = card.getAttribute('data-cat');
                            const cardChains = card.getAttribute('data-chains').toLowerCase();

                            const matchesQ = !q || name.includes(q) || desc.includes(q) || cardChains.includes(q);
                            const matchesCat = !cat || cat === 'All' || cardCat === cat;
                            const matchesChain = !chain || chain === 'All' || cardChains.includes(chain.toLowerCase());

                            if (matchesQ && matchesCat && matchesChain) {
                                card.style.display = 'flex';
                                visibleCount++;
                            } else {
                                card.style.display = 'none';
                            }
                        });

                        const counter = document.getElementById('toolCount');
                        if (counter) counter.innerText = `${visibleCount} tools listed`;
                    }

                    function copyText(btn, text) {
                        navigator.clipboard.writeText(text).then(() => {
                            const orig = btn.innerText;
                            btn.innerText = 'Copied!';
                            btn.classList.add('copied');
                            setTimeout(() => {
                                btn.innerText = orig;
                                btn.classList.remove('copied');
                            }, 2000);
                        });
                    }

                    function openConfigModal(name, command, argsStr, envStr, slug) {
                        const args = argsStr ? argsStr.split(' ').filter(x => x.length > 0) : [];
                        const envVars = envStr ? envStr.split(',').map(x => x.trim()).filter(x => x.length > 0) : [];
                        const envObj = {};
                        envVars.forEach(k => { envObj[k] = `<YOUR_${k}>`; });

                        activeToolData = { name, command, args, envObj, slug };
                        document.getElementById('configModalTitle').innerText = `${name} // Config`;
                        document.getElementById('configModal').style.display = 'flex';
                        switchConfigTab('claude');
                    }

                    function switchConfigTab(tab) {
                        currentTab = tab;
                        document.getElementById('tabClaude').classList.toggle('active', tab === 'claude');
                        document.getElementById('tabCursor').classList.toggle('active', tab === 'cursor');
                        document.getElementById('tabAgy').classList.toggle('active', tab === 'agy');

                        if (!activeToolData) return;
                        const body = document.getElementById('configModalBody');

                        if (tab === 'claude') {
                            const claudeCfg = {
                                "mcpServers": {
                                    [activeToolData.slug]: {
                                        "command": activeToolData.command,
                                        "args": activeToolData.args,
                                        "env": activeToolData.envObj
                                    }
                                }
                            };
                            body.innerText = JSON.stringify(claudeCfg, null, 2);
                        } else if (tab === 'cursor') {
                            const cursorCfg = {
                                "name": activeToolData.slug,
                                "command": activeToolData.command,
                                "args": activeToolData.args,
                                "env": activeToolData.envObj
                            };
                            body.innerText = JSON.stringify(cursorCfg, null, 2);
                        } else if (tab === 'agy') {
                            const argsJoined = activeToolData.args.join(' ');
                            body.innerText = `# Antigravity CLI\nagy mcp add ${activeToolData.slug} -- ${activeToolData.command} ${argsJoined}`;
                        }
                    }

                    function copyCurrentModalConfig() {
                        const content = document.getElementById('configModalBody').innerText;
                        const btn = document.getElementById('btnCopyModal');
                        copyText(btn, content);
                    }

                    function closeConfigModal() {
                        document.getElementById('configModal').style.display = 'none';
                    }

                    function openSubmitModal() {
                        document.getElementById('submitModal').style.display = 'flex';
                    }

                    function closeSubmitModal() {
                        document.getElementById('submitModal').style.display = 'none';
                    }

                    async function handleAnonymousSubmit(e) {
                        e.preventDefault();
                        const btn = document.getElementById('btnSubmitForm');
                        const resDiv = document.getElementById('submitResult');
                        btn.disabled = true;
                        btn.innerText = 'Submitting anonymously...';
                        resDiv.style.display = 'none';

                        const form = e.target;
                        const data = {
                            name: form.name.value,
                            description: form.description.value,
                            category: form.category.value,
                            chains: form.chains.value,
                            command: form.command.value,
                            args: form.args.value || null,
                            env_vars: form.env_vars.value || null,
                            repo_url: form.repo_url.value,
                            docs_url: form.docs_url.value || null,
                            author_alias: form.author_alias.value || null
                        };

                        try {
                            const resp = await fetch('/api/tools', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify(data)
                            });

                            if (resp.ok) {
                                resDiv.style.display = 'block';
                                resDiv.style.color = '#fff';
                                resDiv.innerText = '✓ Submitted successfully! Reloading registry...';
                                setTimeout(() => { window.location.reload(); }, 1200);
                            } else {
                                const err = await resp.text();
                                resDiv.style.display = 'block';
                                resDiv.style.color = '#ff6b6b';
                                resDiv.innerText = `Error: ${err}`;
                                btn.disabled = false;
                                btn.innerText = 'Submit Tool Anonymously';
                            }
                        } catch (err) {
                            resDiv.style.display = 'block';
                            resDiv.style.color = '#ff6b6b';
                            resDiv.innerText = `Network error: ${err.message}`;
                            btn.disabled = false;
                            btn.innerText = 'Submit Tool Anonymously';
                        }
                    }

                    // Close on Escape or click outside
                    window.addEventListener('keydown', (e) => {
                        if (e.key === 'Escape') {
                            closeSubmitModal();
                            closeConfigModal();
                        }
                    });
                    "#))
                }
            }
        }
    }
}
