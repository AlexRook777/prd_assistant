# Test Page Style Guide

This guide defines the standard UI/UX for all generated test pages. You **MUST** use the CSS and HTML structure defined below to ensure consistency across different integrations.

## 1. CSS Styles
Include this exact CSS block in the `<head>` of the generated HTML page.

```css
:root {
    --primary: #00ff88;
    --primary-dark: #00cc6e;
    --bg: #0f172a;
    --card-bg: #1e293b;
    --text: #f8fafc;
    --text-dim: #94a3b8;
    --border: #334155;
    --error: #ef4444;
    --success: #22c55e;
    --warning: #f59e0b;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg);
    color: var(--text);
    line-height: 1.5;
    padding: 1rem;
    margin: 0;
    height: 100vh;
    overflow: hidden;
}

.container {
    max-width: 100%;
    height: calc(100vh - 2rem);
    margin: 0 auto;
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    grid-template-rows: auto 1fr;
    gap: 1rem;
}

h1, h2, h3 {
    margin-bottom: 1rem;
    font-weight: 600;
}

h1 {
    grid-column: 1 / -1;
    text-align: center;
    color: var(--primary);
    font-size: 1.75rem;
    margin-bottom: 0.5rem;
    text-shadow: 0 0 20px rgba(0, 255, 136, 0.2);
}

.card {
    background-color: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    overflow-y: auto;
    height: 100%;
}

.form-group {
    margin-bottom: 1rem;
}

label {
    display: block;
    font-size: 0.875rem;
    font-weight: 500;
    color: var(--text-dim);
    margin-bottom: 0.25rem;
}

input, select, textarea {
    width: 100%;
    background-color: #0f172a;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.5rem 0.75rem;
    color: var(--text);
    font-family: inherit;
    font-size: 0.875rem;
    transition: border-color 0.2s;
}

input:focus {
    outline: none;
    border-color: var(--primary);
}

.button-group {
    display: flex;
    gap: 0.5rem;
    margin-top: 1rem;
}

button {
    background-color: var(--primary);
    color: #0f172a;
    border: none;
    border-radius: 6px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
}

button:hover {
    background-color: var(--primary-dark);
    transform: translateY(-1px);
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}

button.secondary {
    background-color: transparent;
    border: 1px solid var(--primary);
    color: var(--primary);
}

button.secondary:hover {
    background-color: rgba(0, 255, 136, 0.1);
}

button.danger {
    background-color: transparent;
    border: 1px solid var(--error);
    color: var(--error);
}

button.danger:hover {
    background-color: rgba(239, 68, 68, 0.1);
}

.log-container, .webhook-container {
    flex: 1;
    overflow-y: auto;
    background-color: #0c111d;
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 0.75rem;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.7rem;
}

.log-entry, .webhook-entry {
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #1e293b;
}

.log-entry:last-child, .webhook-entry:last-child {
    border-bottom: none;
}

.log-meta {
    display: flex;
    justify-content: space-between;
    color: var(--text-dim);
    margin-bottom: 0.5rem;
}

.status-badge {
    padding: 0.125rem 0.375rem;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
}

.status-pending { background-color: #f59e0b; color: #fff; }
.status-success { background-color: #22c55e; color: #fff; }
.status-failed { background-color: #ef4444; color: #fff; }

pre {
    white-space: pre-wrap;
    word-break: break-all;
    color: #e2e8f0;
}

.copy-btn {
    background: none;
    border: none;
    color: var(--primary);
    cursor: pointer;
    font-size: 0.7rem;
    padding: 0;
    text-decoration: underline;
}

.logs-webhooks-column {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    height: 100%;
}

.logs-section, .webhooks-section {
    display: flex;
    flex-direction: column;
    flex: 1;
    min-height: 0;
}

.section-title {
    font-size: 1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: var(--primary);
}

.loading-spinner {
    width: 1rem;
    height: 1rem;
    border: 2px solid rgba(15, 23, 42, 0.3);
    border-top-color: #0f172a;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

#payment-link-container {
    margin-top: 1rem;
    padding: 1rem;
    background-color: rgba(0, 255, 136, 0.1);
    border: 1px solid var(--primary);
    border-radius: 6px;
    display: none;
}

#payment-link-container a {
    color: var(--primary);
    word-break: break-all;
}

/* Toggle Switch */
.switch-container {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}

.switch {
    position: relative;
    display: inline-block;
    width: 48px;
    height: 24px;
}

.switch input {
    opacity: 0;
    width: 0;
    height: 0;
}

.slider {
    position: absolute;
    cursor: pointer;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: #334155;
    transition: .4s;
    border-radius: 24px;
}

.slider:before {
    position: absolute;
    content: "";
    height: 18px;
    width: 18px;
    left: 3px;
    bottom: 3px;
    background-color: white;
    transition: .4s;
    border-radius: 50%;
}

input:checked + .slider {
    background-color: var(--primary);
}

input:focus + .slider {
    box-shadow: 0 0 1px var(--primary);
}

input:checked + .slider:before {
    transform: translateX(24px);
}
```

## 2. HTML Structure Recommendation

### Main Layout
```html
<body>
    <div class="container">
        <h1>[Integration Name] Testing Console</h1>

        <!-- Left Column: Credentials & Config -->
        <div class="card">
            <h2>API Credentials</h2>
            <div class="form-group"> ... </div>
            <!-- ... -->
        </div>

        <!-- Middle Column: Transaction Actions -->
        <div class="card">
            <h2>Create Transaction</h2>
            <div class="form-group"> ... </div>
            <!-- ... -->
        </div>

        <!-- Right Column: Logs & Webhooks (Split Vertically) -->
        <div class="logs-webhooks-column">
            <!-- API Logs Section -->
            <div class="logs-section">
                <h3 class="section-title">API Logs</h3>
                <div id="api-logs" class="log-container"> ... </div>
            </div>

            <!-- Webhooks Section -->
            <div class="webhooks-section">
                <h3 class="section-title">Webhooks</h3>
                <div id="webhook-logs" class="webhook-container"> ... </div>
            </div>
        </div>
    </div>
</body>
```

### Standard Components

#### Loading Button
```html
<button id="btn-action">
    <span>Action Name</span>
</button>
<!-- JS Helper needed to inject .loading-spinner into span when active -->
```

#### Log Entry Structure
```html
<div class="log-entry">
    <div class="log-meta">
        <span>TIMESTAMP | METHOD URL</span>
        <span class="status-badge status-success">200</span>
    </div>
    <div><strong>Headers:</strong> <pre>...</pre></div>
    <div><strong>Body:</strong> <pre>...</pre></div>
    <button class="copy-btn">Copy Entry</button>
</div>
```
