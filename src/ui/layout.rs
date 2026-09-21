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
                meta name="description" content="Anonymous Web3 Model Context Protocol (MCP) Directory & Marketplace. Zero KYC, zero OAuth, pure non-custodial listing & monetization.";
                style { (CSS) }
            }
            body {
                header {
                    div class="container header-inner" {
                        div class="brand" {
                            a href="/" class="brand-title" { "WEB3-MCP // MARKETPLACE" }
                            span class="badge-anon" { "ZERO-KYC" }
                            span class="badge-anon" { "NON-CUSTODIAL" }
                            span class="badge-anon" { "100% RUST" }
                        }
                        nav {
                            a href="/" { "Directory & Market" }
                            a href="/api/tools" target="_blank" { "JSON API" }
                            a href="/api/export" download="web3-mcp-directory.json" { "Export" }
                            button class="btn-submit-nav" onclick="openSubmitModal()" { "+ Jual / List Tool" }
                        }
                    }
                }

                main {
                    (content)
                }

                footer {
                    div class="container footer-inner" {
                        div {
                            "Built with Rust (Axum + Maud + SQLite). Tanpa rekening bank, tanpa Stripe KYC, tanpa fee perantara. Pembayaran 100% P2P on-chain."
                        }
                        div {
                            "Protocol: Cypherpunk Commerce // M2M Native"
                        }
                    }
                }

                // Global Submission / Listing Modal (Jual & Listing Tanpa Birokrasi)
                div id="submitModal" class="modal-overlay" style="display: none;" {
                    div class="modal-content" {
                        div class="modal-header" {
                            span class="modal-title" { "Jual / Daftarkan Web3 MCP Tool (Full Anonim)" }
                            button class="btn-close" onclick="closeSubmitModal()" { "×" }
                        }
                        p style="font-size: 12px; color: var(--text-muted); margin-bottom: 16px;" {
                            "Nol birokrasi: Tanpa verifikasi KTP/KYC, tanpa rekening bank Web2, tanpa akun Stripe. Pembeli/pengguna langsung mentransfer kripto ke wallet pribadi kamu."
                        }
                        form id="submitForm" onsubmit="handleAnonymousSubmit(event)" {
                            div class="form-group" {
                                label class="form-label" { "Nama Tool / MCP Server *" }
                                input type="text" name="name" required class="form-input" placeholder="e.g. Flashloan Arbitrage Hunter MCP";
                            }
                            div class="form-group" {
                                label class="form-label" { "Deskripsi & Value Proposition *" }
                                textarea name="description" required rows="2" class="form-textarea" placeholder="Jelaskan fungsi tool, endpoint yang diexpose, atau keuntungan finansial bagi agent/user..." {}
                            }
                            div style="display: flex; gap: 10px;" {
                                div class="form-group" style="flex: 1;" {
                                    label class="form-label" { "Kategori *" }
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
                                    input type="text" name="chains" required class="form-input" placeholder="e.g. Ethereum, Base, Solana, Arbitrum";
                                }
                            }

                            // Monetization section
                            div style="border: 1px solid #333; padding: 12px; margin-bottom: 14px; background: #0a0a0a;" {
                                span style="font-size: 11px; font-family: var(--mono-font); color: #aaa; text-transform: uppercase; display: block; margin-bottom: 8px;" {
                                    "// Model Monetisasi & Payout (Langsung ke Wallet Kamu)"
                                }
                                div style="display: flex; gap: 10px;" {
                                    div class="form-group" style="flex: 1; margin-bottom: 8px;" {
                                        label class="form-label" { "Model Penjualan *" }
                                        select name="pricing_model" required class="form-select" {
                                            option value="Free & Open Source" { "Free & Open Source" }
                                            option value="Crypto License" { "Crypto License (Jual Akses/Kunci)" }
                                            option value="Pay-per-Call (x402)" { "Pay-per-Call (HTTP 402/x402)" }
                                            option value="Tipping / Donation" { "Donasi / Tipping Kripto" }
                                        }
                                    }
                                    div class="form-group" style="flex: 1; margin-bottom: 8px;" {
                                        label class="form-label" { "Harga / Biaya *" }
                                        input type="text" name="price" required class="form-input" placeholder="e.g. 0.08 ETH, $5 USDC / mo, Free";
                                    }
                                }
                                div class="form-group" style="margin-bottom: 8px;" {
                                    label class="form-label" { "Wallet Payout Address (EVM / Solana / BTC / Monero)" }
                                    input type="text" name="payout_address" class="form-input" placeholder="0x... atau alamat wallet kamu untuk menerima pembayaran langsung";
                                }
                                div class="form-group" style="margin-bottom: 0;" {
                                    label class="form-label" { "Link Penjualan / Kontak Pembelian (Opsional)" }
                                    input type="url" name="commercial_url" class="form-input" placeholder="https://t.me/anon_dev atau link dApp paywall";
                                }
                            }

                            div style="display: flex; gap: 10px;" {
                                div class="form-group" style="flex: 1;" {
                                    label class="form-label" { "Executable / Command *" }
                                    input type="text" name="command" required class="form-input" placeholder="e.g. npx, docker, cargo, python";
                                }
                                div class="form-group" style="flex: 2;" {
                                    label class="form-label" { "Arguments" }
                                    input type="text" name="args" class="form-input" placeholder="e.g. -y @package/name --network mainnet";
                                }
                            }
                            div class="form-group" {
                                label class="form-label" { "Required Env Vars (comma separated)" }
                                input type="text" name="env_vars" class="form-input" placeholder="e.g. RPC_URL, PRIVATE_KEY";
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
                                label class="form-label" { "Author / Creator Alias (Default: 0xAnon)" }
                                input type="text" name="author_alias" class="form-input" placeholder="0xAnon / vitalik.eth / pseudonym";
                            }
                            button type="submit" id="btnSubmitForm" class="btn-primary" {
                                "Listing & Siap Dijual Tanpa Birokrasi"
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

                // Direct Non-Custodial Crypto Payment / Tip Modal
                div id="paymentModal" class="modal-overlay" style="display: none;" {
                    div class="modal-content" {
                        div class="modal-header" {
                            span id="paymentModalTitle" class="modal-title" { "Direct Non-Custodial Payment" }
                            button class="btn-close" onclick="closePaymentModal()" { "×" }
                        }
                        div style="margin-bottom: 16px;" {
                            p id="paymentModalDesc" style="font-size: 13px; color: var(--text-muted); margin-bottom: 10px;" {}
                            div style="background: #080808; border: 1px solid var(--border); padding: 12px; margin-bottom: 12px;" {
                                div style="font-size: 11px; color: var(--text-dim); margin-bottom: 4px; font-family: var(--mono-font);" {
                                    "CREATOR RECEIVING WALLET ADDRESS:"
                                }
                                div id="paymentModalAddress" class="code-box" style="word-break: break-all; font-size: 13px; color: #fff; padding: 8px;" {}
                            }
                            p style="font-size: 11px; color: var(--text-dim);" {
                                "⚡ Dana langsung masuk ke wallet pembuat tool tanpa perantara bank, tanpa potongan fee platform, dan tanpa Stripe KYC."
                            }
                        }
                        div style="display: flex; justify-content: flex-end; gap: 8px;" {
                            button class="btn-action" id="btnCopyAddress" onclick="copyPaymentAddress()" { "Copy Wallet Address" }
                            button class="btn-action" onclick="closePaymentModal()" { "Close" }
                        }
                    }
                }

                script {
                    (maud::PreEscaped(r#"
                    let activeToolData = null;
                    let currentTab = 'claude';
                    let currentPayoutAddress = '';

                    function filterTools() {
                        const q = document.getElementById('searchInput').value.toLowerCase().trim();
                        const cat = document.getElementById('categoryFilter').value;
                        const chain = document.getElementById('chainFilter').value;
                        const pricing = document.getElementById('pricingFilter').value;
                        const cards = document.querySelectorAll('.card');
                        let visibleCount = 0;

                        cards.forEach(card => {
                            const name = card.getAttribute('data-name').toLowerCase();
                            const desc = card.getAttribute('data-desc').toLowerCase();
                            const cardCat = card.getAttribute('data-cat');
                            const cardChains = card.getAttribute('data-chains').toLowerCase();
                            const cardPricing = card.getAttribute('data-pricing');

                            const matchesQ = !q || name.includes(q) || desc.includes(q) || cardChains.includes(q) || cardPricing.toLowerCase().includes(q);
                            const matchesCat = !cat || cat === 'All' || cardCat === cat;
                            const matchesChain = !chain || chain === 'All' || cardChains.includes(chain.toLowerCase());
                            const matchesPricing = !pricing || pricing === 'All' || cardPricing === pricing;

                            if (matchesQ && matchesCat && matchesChain && matchesPricing) {
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

                    function openPaymentModal(toolName, model, price, payoutAddress) {
                        currentPayoutAddress = payoutAddress;
                        document.getElementById('paymentModalTitle').innerText = `${toolName} // Direct Payout`;
                        document.getElementById('paymentModalDesc').innerHTML = `Model: <strong>${model}</strong> | Harga: <strong>${price}</strong>`;
                        document.getElementById('paymentModalAddress').innerText = payoutAddress;
                        document.getElementById('paymentModal').style.display = 'flex';
                    }

                    function copyPaymentAddress() {
                        const btn = document.getElementById('btnCopyAddress');
                        copyText(btn, currentPayoutAddress);
                    }

                    function closePaymentModal() {
                        document.getElementById('paymentModal').style.display = 'none';
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
                        btn.innerText = 'Menyimpan & mendaftarkan ke direktori...';
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
                            author_alias: form.author_alias.value || null,
                            pricing_model: form.pricing_model.value,
                            price: form.price.value,
                            payout_address: form.payout_address.value || null,
                            commercial_url: form.commercial_url.value || null
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
                                resDiv.innerText = '✓ Berhasil terdaftar secara instan! Memuat ulang direktori...';
                                setTimeout(() => { window.location.reload(); }, 1200);
                            } else {
                                const err = await resp.text();
                                resDiv.style.display = 'block';
                                resDiv.style.color = '#ff6b6b';
                                resDiv.innerText = `Error: ${err}`;
                                btn.disabled = false;
                                btn.innerText = 'Listing & Siap Dijual Tanpa Birokrasi';
                            }
                        } catch (err) {
                            resDiv.style.display = 'block';
                            resDiv.style.color = '#ff6b6b';
                            resDiv.innerText = `Network error: ${err.message}`;
                            btn.disabled = false;
                            btn.innerText = 'Listing & Siap Dijual Tanpa Birokrasi';
                        }
                    }

                    // Close on Escape or click outside
                    window.addEventListener('keydown', (e) => {
                        if (e.key === 'Escape') {
                            closeSubmitModal();
                            closeConfigModal();
                            closePaymentModal();
                        }
                    });
                    "#))
                }
            }
        }
    }
}
