pub const CSS: &str = r#"
*, *::before, *::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

:root {
  --bg: #0d0d0d;
  --surface: #141414;
  --surface-hover: #1a1a1a;
  --border: #262626;
  --border-focus: #555555;
  --text: #e5e5e5;
  --text-muted: #888888;
  --text-dim: #555555;
  --mono-font: 'JetBrains Mono', 'SFMono-Regular', Consolas, Menlo, monospace;
  --sans-font: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

body {
  background-color: var(--bg);
  color: var(--text);
  font-family: var(--sans-font);
  line-height: 1.5;
  font-size: 14px;
  -webkit-font-smoothing: antialiased;
}

a {
  color: inherit;
  text-decoration: none;
}

button, input, select, textarea {
  font-family: inherit;
  font-size: inherit;
  color: inherit;
  background: transparent;
  border: 1px solid var(--border);
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Header */
header {
  border-bottom: 1px solid var(--border);
  padding: 16px 0;
  background: var(--bg);
  position: sticky;
  top: 0;
  z-index: 50;
}

.header-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-title {
  font-family: var(--mono-font);
  font-weight: 700;
  font-size: 15px;
  letter-spacing: -0.5px;
}

.badge-anon {
  font-family: var(--mono-font);
  font-size: 11px;
  padding: 2px 6px;
  border: 1px solid var(--border);
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

nav {
  display: flex;
  align-items: center;
  gap: 16px;
  font-family: var(--mono-font);
  font-size: 13px;
}

nav a {
  color: var(--text-muted);
}

nav a:hover, nav a.active {
  color: var(--text);
}

.btn-submit-nav {
  padding: 5px 12px;
  border: 1px solid var(--text);
  color: var(--text);
  cursor: pointer;
}

.btn-submit-nav:hover {
  background: var(--text);
  color: var(--bg);
}

/* Hero */
.hero {
  padding: 40px 0 24px;
  border-bottom: 1px solid var(--border);
}

.hero h1 {
  font-size: 24px;
  font-weight: 600;
  letter-spacing: -0.5px;
  margin-bottom: 8px;
}

.hero p {
  color: var(--text-muted);
  font-size: 14px;
  max-width: 680px;
}

/* Controls / Filters */
.controls {
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.search-row {
  display: flex;
  gap: 10px;
}

.search-input {
  flex: 1;
  padding: 10px 14px;
  background: var(--surface);
  border: 1px solid var(--border);
  outline: none;
  font-family: var(--mono-font);
  font-size: 13px;
}

.search-input:focus {
  border-color: var(--border-focus);
}

.filter-row {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
}

.filter-select {
  padding: 8px 12px;
  background: var(--surface);
  border: 1px solid var(--border);
  outline: none;
  cursor: pointer;
  font-size: 13px;
}

.filter-select:focus {
  border-color: var(--border-focus);
}

.counter {
  margin-left: auto;
  font-family: var(--mono-font);
  font-size: 12px;
  color: var(--text-muted);
}

/* Grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 16px;
  padding: 10px 0 60px;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  padding: 18px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 14px;
  transition: border-color 0.15s ease;
}

.card:hover {
  border-color: var(--border-focus);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 4px;
}

.card-meta {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-top: 4px;
}

.tag {
  font-family: var(--mono-font);
  font-size: 11px;
  padding: 2px 6px;
  border: 1px solid var(--border);
  color: var(--text-muted);
}

.tag-verified {
  color: #fff;
  border-color: #444;
}

.card-desc {
  color: var(--text-muted);
  font-size: 13px;
  line-height: 1.45;
  flex-grow: 1;
}

.code-box {
  background: #080808;
  border: 1px solid var(--border);
  padding: 8px 10px;
  font-family: var(--mono-font);
  font-size: 11px;
  color: #ccc;
  overflow-x: auto;
  white-space: nowrap;
}

.card-actions {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  padding-top: 10px;
  border-top: 1px solid var(--border);
}

.btn-action {
  padding: 5px 9px;
  font-size: 11px;
  font-family: var(--mono-font);
  cursor: pointer;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text-muted);
}

.btn-action:hover {
  color: var(--text);
  border-color: var(--border-focus);
}

.btn-action.copied {
  color: #fff;
  border-color: #888;
}

/* Modal / Form */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 20px;
}

.modal-content {
  background: var(--surface);
  border: 1px solid var(--border);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  padding: 24px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--border);
}

.modal-title {
  font-size: 16px;
  font-weight: 600;
  font-family: var(--mono-font);
}

.btn-close {
  border: none;
  cursor: pointer;
  font-size: 16px;
  color: var(--text-muted);
}

.btn-close:hover {
  color: var(--text);
}

.form-group {
  margin-bottom: 14px;
}

.form-label {
  display: block;
  font-size: 12px;
  font-family: var(--mono-font);
  color: var(--text-muted);
  margin-bottom: 4px;
}

.form-input, .form-textarea, .form-select {
  width: 100%;
  padding: 8px 10px;
  background: #0d0d0d;
  border: 1px solid var(--border);
  outline: none;
  font-family: var(--mono-font);
  font-size: 12px;
}

.form-input:focus, .form-textarea:focus, .form-select:focus {
  border-color: var(--border-focus);
}

.form-help {
  font-size: 11px;
  color: var(--text-dim);
  margin-top: 3px;
}

.btn-primary {
  width: 100%;
  padding: 10px;
  background: var(--text);
  color: var(--bg);
  font-weight: 600;
  font-family: var(--mono-font);
  font-size: 13px;
  cursor: pointer;
  border: none;
  margin-top: 10px;
}

.btn-primary:hover {
  opacity: 0.9;
}

/* Footer */
footer {
  border-top: 1px solid var(--border);
  padding: 30px 0;
  margin-top: 40px;
  color: var(--text-muted);
  font-size: 12px;
  font-family: var(--mono-font);
}

.footer-inner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.raw-json-modal {
  display: none;
}
"#;
