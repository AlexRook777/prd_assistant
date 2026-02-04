---
description: Phase 1 Step 4 - Automate test page verification and fixing
---

// turbo-all

# Step 4: Automate Test Page

> [!IMPORTANT]
> **AUTONOMOUS EXECUTION MODE**: This workflow runs fully autonomously without user confirmation.
> - Execute ALL browser interactions, file edits, and commands with `SafeToAutoRun: true`
> - Act like a confident QA engineer who knows exactly what to do
> - DO NOT ask for confirmation for any test page manipulation, form filling, button clicks, or HTML fixes
> - Make decisions independently based on observed results and error messages
> - Only stop to report final results or after max retry attempts

Automatically test the generated `3.test_page.html` using a browser agent. If issues are found, the agent will attempt to fix the HTML file and retry.

## Working Directory
`<current_integration>/1_result/`

## Prerequisites
- `3.test_page.html` must exist (Run Step 3a first).
- `serve.py` must be running (The workflow handles this).

## Task

1. **Ensure Server is Running**:
   - **Check**: Is port 8000 occupied?
   - **Linux**: `fuser -k 8000/tcp` followed by `nohup python3 app/serve.py > /dev/null 2>&1 &` (run from repo root)
   - **Mac**: `lsof -ti:8000 | xargs kill -9` followed by `nohup python3 app/serve.py > /dev/null 2>&1 &`
   - **Windows**: `taskkill /F /IM python.exe /T` (to kill) -> `start /B python app/serve.py`
   - **WAIT** 2 seconds for server to start.

2. **Pre-Flight Checks** (Before opening browser):
   - **Enable Proxy**: Always enable "Use Proxy" toggle to avoid CORS errors.
   - **Generate Unique ID**: If the Transaction ID field is empty or contains a literal template string, generate a unique ID using JavaScript: `'order_' + Date.now()`.
   - **Verify Webhook Mode**: If testing webhooks, ensure N8n mode is enabled and the Order ID in the info box matches the Transaction ID field.

3. **Loop: Test & fix**:
   - **Goal**: Successfully create a transaction and verify status.
   - **EXECUTION MODE**: Run browser subagent autonomously - NO user confirmations needed for any action.
   - **Action**:
         - Use `open_browser` to navigate to `http://localhost:8000/integrations/<Integration_Name>/1_result/3.test_page.html`.
         - Fill in credentials from `integration_config`.
         - Click "Get Token" (if applicable).
         - Click "Create Transaction".
         - **Verify**: Did it succeed?
           - **YES**: 
             - **Webhook Verification (Optional N8n)**:
               - If the test page supports n8n webhooks, verify webhook delivery.
               - Use the **N8n Webhook Tester** skill (`.agent/skills/n8n_webhook_tester/SKILL.md`).
               - Poll for webhooks using the order ID from the transaction.
               - Document webhook payloads in the test results.
             - Take screenshot.
             - Create `1_result/4.auto_test_page.md` with a **Detailed Test Log**:
               - **General Status**: Success/Fail.
               - **Step-by-Step Log**: Detailed actions and results for Token, Transaction, and Webhook.
               - **Webhook Results**: Include n8n webhook verification if performed.
               - **Issues & Fixes**: List any issues encountered, what caused them, and how they were fixed.
               - **Workflow Suggestions**: Suggest improvements for future phases based on findings.
               - **Screenshots**: Embed successful transaction screenshots.
             - Stop.
       - **NO**:
         - Analyse the error (Console logs, UI error message).
         - **Fix**: Edit `3.test_page.html` to correct the issue (e.g., incorrect field name, missing header, wrong JSON format).
         - **Retry**: Reload page and try again.
         - **Limit**: Max 5 fix attempts. If still failing, create `1_result/4.auto_test_page.md` with "Issues Found" section and Stop.

4. **Output**:
   - Updated `3.test_page.html` (if fixes were needed).
   - Created `4.auto_test_page.md` with test results and screenshots.
   - Include `## Workflow Suggestions` section at the end (see `.gemini.md` for format).

---

## Known Issues & Best Practices

> [!TIP]
> These are common issues encountered during automated testing. The agent should proactively check for and fix them.

| Issue | Symptom | Fix |
|-------|---------|-----|
| **CORS Errors** | `Access-Control-Allow-Origin` errors in console | Always enable "Use Proxy" toggle before any API calls |
| **Literal Template String** | Transaction ID field shows `${Date.now()}` literally | Use JS to set value: `document.getElementById('transaction-id').value = 'order_' + Date.now()` |
| **Token Not Populating** | Access Token field stays empty after "Get Token" | Check for nested response: `data.access_token \|\| data.data?.access_token` |
| **Wrong Webhook UUID** | Refresh button returns empty despite webhooks sent | Verify `refreshWebhooks` uses the **send** UUID (`0154f998...`), not retrieve UUID |
| **Sandbox Webhooks Delayed** | No webhooks within 60s | Sandbox often requires manual payment completion; document as expected behavior |

### N8n Webhook Endpoints Reference
- **Send URL** (provider calls this): `https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b/{orderId}`
- **Retrieve URL** (we poll this): `https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b/{orderId}` (same as send)
- **Auth**: `Basic btoa('callbacks-test:callbacks-test123')`

---

## Success Criteria
- `4.auto_test_page.md` is created and contains a "Test Results" section.