---
name: Test Page Generator
description: Generate functional HTML test pages for payment provider API verification with webhook testing support
---

# Test Page Generator Skill

## When to Use This Skill
Automatically activate when user mentions:
- "create test page" or "generate test page"
- "Step 3" or "create test page" in research context
- Testing payment provider APIs
- HPP (Hosted Payment Page) testing

This skill is specifically designed for **Phase 1, Step 3** of the integration workflow.


## Prerequisites
- `global_config` file **NO LONGER REQUIRED** to have `TEST_POST_WEBHOOK_URL` as we use local `serve.py`.

## Task Description

### Phase 1: Create Test Page

**Step 1**: Create a test HTML page with **3-column layout** using **Compact Mode**:
- **Design Goal**: Maximize information density. Eliminate scrolling. Use `height: 100vh` and tight spacing.
- **Global Settings**: `line-height: 1.3`, base font size `0.8rem` or smaller.
- **Column 1**: API Credentials ...
- **Column 3**: Page Title (H1) at the top, followed by API Logs and Webhooks.
- The "API Credentials" card header must have a toggle switch on the right side.
- The "Webhook Configuration" section (below Get Token button) must have a toggle switch on the right side of its title.
- **Toggle Naming Convention**: Labels show the **current active mode**, not the action:
  - Proxy toggle: "Direct API" (OFF) or "Proxy" (ON)
  - Webhook toggle: "Local Webhooks" (OFF) or "N8n Webhooks" (ON)
- **Default States**: Both toggles should be **ON by default** (checked):
  - Proxy: ON (routes through `http://localhost:8000/proxy`)
  - Webhooks: ON (uses N8n webhooks)
- If Proxy enabled, all API requests (OAuth, Transaction, Status) must be routed through `http://localhost:8000/proxy`.
- If Proxy disabled, requests go directly to the provider's API.
- The page must allow the user to:
    - Enter all required credentials
    - Receive a payment link
    - Open the payment link in a new tab
    - Check payment status via a button
    - View updated payment status within the payment details on the page

**Step 2**: Logs and Webhooks Display:
- **API Logs** section at the top of the third column (Flex 1) with "Clear" button
- **Webhooks** section at the bottom of the third column (Flex 1) with "Refresh" and "Clear" buttons
- Both sections visible simultaneously (no tab switching)
- Each section has independent scrolling
- **Log Order**: Newest entries appear at the TOP of the list (reverse chronological)
- Option to view and copy all requests and responses (including headers)
- Request log with individual entry copy functionality

**Step 3**: Design and Logic Requirements.
- **MANDATORY**: You **MUST** use the standard CSS and HTML structure definitions from `resources/style_guide.md`. Read this file before generating the HTML.
- **Layout Structure**:
    - **3-column grid**: `gap: 0.5rem`, `grid-template-rows: 1fr` (No separate header row)
    - **No scrolling**: Page fits within viewport (`height: 100vh`, `overflow: hidden`)
    - **Third column**: Title (H1) -> API Logs (Flex) -> Webhooks (Flex)
    - **Compact CSS**: Use reduced padding (`0.5rem` or less) and margins (`0.5rem` or less) throughout.
    - **Access Token Layout**: Use grid layout to position Get Token button on left, Access Token field on right:
      ```html
      <div style="display: grid; grid-template-columns: auto 1fr; gap: 1rem; align-items: start;">
          <button id="btn-get-token">Get Token</button>
          <div class="form-group" style="margin: 0;">
              <label for="access-token">Access Token</label>
              <textarea id="access-token" rows="3" readonly></textarea>
          </div>
      </div>
      ```
    - **Webhook Configuration**: Must be placed in Column 1 (API Credentials), below the Get Token button, with toggle on the right of the section title
- **Proxy Logic**:
    - **Default State**: Proxy toggle should be **checked (ON)** by default
    - **Header Layout**: Use `<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;"><h2>API Credentials</h2><div class="switch-container">...</div></div>`.
    - **Toggle Label**: Must show current mode - "Direct API" when OFF, "Proxy" when ON
    - **Toggle Function**: Create `toggleProxyMode()` function that updates the label based on checkbox state
    - **Persistence**: Save the switch state in `sessionStorage` (key: `use-proxy-toggle`).
    - **Request Format (Proxy ON)**:
        - URL: `http://localhost:8000/proxy`
        - Method: `POST`
        - Body: `JSON.stringify({ url: targetUrl, method: targetMethod, headers: targetHeaders, body: targetBody })`
    - **Response Handling (Proxy ON)**:
        - The proxy *always* returns 200 if the proxying succeeded.
        - The actual upstream response is in the JSON body: `{ status: <int>, headers: <dict>, body: <string|obj> }`.
        - **CRITICAL**: The `body` from the proxy might be a JSON **string** (serialized) or an object. You **MUST** check if `data.body` is a string and, if so, `JSON.parse()` it before using it.
        - You MUST unwrap this to treat it effectively as the real response (e.g., use `data.status` for success checks).
    - **Robust Parsing**: Handle nested JSON responses (e.g., `data.data.access_token` vs `data.access_token`). Check multiple common paths for tokens and links:
      ```javascript
      const token = data.access_token || (data.data && data.data.access_token);
      ```
    - **Dynamic ID Generation** (MANDATORY):
      - The Transaction ID field MUST NOT contain literal template strings (e.g., `${Date.now()}`).
      - On page load, if the field is empty, generate a unique ID: `'order_' + Date.now()`.
      - Example:
        ```javascript
        if (!document.getElementById('transaction-id').value) {
            document.getElementById('transaction-id').value = 'order_' + Date.now();
        }
        ```
- **Valid Data**: Use valid, check-summed national IDs (CI, CPF) by default. VALIDATE document types (e.g., 'CI' vs 'CC').
- **Comprehensive Field Coverage**:
    - **Analyze API Params**: You MUST read `1_result/2.docs_analysis.md` to identify **ALL** parameters for the transaction endpoint (mandatory AND optional).
    - **Field Completeness**: You MUST include input fields for **ALL** parameters identified in the analysis. Do NOT skip optional fields.
    - **No Hardcoding**: Create UI inputs for ALL identified parameters. Do NOT hardcode values in the JS logic (except for sensible defaults in the input `value` attribute).
    - **Critical Fields**: Ensure you include inputs for often-missed fields such as:
        - `currency`, `country`
        - `payment_method` (e.g., as a text input or select)
        - `notification_url` / `callback_url`
        - `customer.email`, `customer.phone`, `customer.address`
        - `customer.document.type` (if applicable)
    - **Format Hints**: Provide placeholder text or labels indicating required formats, especially:
        - Phone numbers (e.g., "E.164 format: +593...")
        - Dates (e.g., "YYYY-MM-DD")
        - IDs (e.g., "CPF", "CI")
    - **Sorting & Grouping**:
        - **Sort Order**: strict "Mandatory First, then Optional".
        - **Grouping**: Within those two primary categories, group fields logically (e.g., Customer info together, Transaction info together).
    - **Layout Rules**:
        - If there are **more than 6 fields** total in a section (e.g., "Create Transaction"), you **MUST** use a 2-column grid layout.
        - If 6 or fewer, use a single column.
    - **UI Indicators**:
        - Mark all mandatory fields with a red asterisk (*) in the label.
        - Use CSS to style the asterisk appropriately (e.g., `color: var(--error)`).
- **Standard Fields**: Include `email`, `phone`, `name`, `document` in the form payload *even if* documentation says optional. Sandbox often requires them.
- Save all entered credentials in `sessionStorage` so they persist on page reload (including the proxy switch state)
- Clear credentials when the browser is closed
- Use a clean, modern design with proper form validation

**Step 4**: Webhook Verification
- **Default State**: Webhook toggle should be **checked (ON)** by default (N8n mode)
- **Webhook Mode Toggle**:
  - Add a toggle switch in the "Webhook Configuration" section (in Column 1, below Get Token) to choose between modes
  - Position toggle to the right of "Webhook Configuration" title (same pattern as Proxy toggle)
  - **Toggle Label**: Must show current mode - "Local Webhooks" when OFF, "N8n Webhooks" when ON
  - **Toggle Function**: Create `toggleWebhookMode()` function that updates the label based on checkbox state
  - Save the webhook mode preference in `sessionStorage`.
- **Local Webhook Mode** (toggle OFF):
  - **Hardcode** the webhook URL to `http://localhost:8000/webhook`.
  - **Hardcode** the polling endpoint to `http://localhost:8000/api/webhooks`.
- **N8n Webhook Mode** (toggle ON - default):
  - Generate a unique order ID using `crypto.randomUUID()` when creating a transaction.
  - Construct webhook URL: `https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b/{orderId}`
  - Use this URL as the callback/notification URL in the transaction request.
  - Poll for webhooks at: `https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b/{orderId}` **(SAME as send URL)**
  - **IMPORTANT**: The send and retrieve URLs use the **same** UUID. Do NOT use a different UUID for retrieval.
  - Use Basic Auth: `btoa('callbacks-test:callbacks-test123')`
  - Display the order ID prominently in the UI for reference.
- **EMBED THE WEBHOOK VIEWER UI**:
  - Create a dedicated section in the third column (bottom half, flex-grow) for webhooks.
  - **NO TABS**: Webhooks section is always visible below API Logs.
  - It MUST include:
    - Auto-polling every 5 seconds.
    - "Refresh" and "Clear" buttons (Clear logs via `DELETE /api/webhooks` for local mode).
    - Expandable details for Body and Headers.
    - Copy buttons.
    - Display current webhook mode (Local/N8n) and order ID (if N8n mode).
- **Display Order**: Webhooks in reverse chronological order (newest first at the top).
- Expected webhook response format from `http://localhost:8000/api/webhooks`:
  ```json
  [
    {
      "method": "POST",
      "headers": {...},
      "body": {...},
      "timestamp": "2026-01-28T07:36:33.640932"
    }
  ]
  ```
- Expected webhook response format from n8n endpoint:
  ```json
  [
    {
      "transaction_id": "TXN123",
      "status": "paid",
      "amount": 100.50,
      "timestamp": "2026-02-04T18:30:00Z"
    }
  ]
  ```

### Phase 2: Automation Testing (Optional - Agent-Driven)

If requested, execute automated testing:
1. Open the test page in a browser with CORS proxy
2. Enter all required credentials and click "Get Token"
3. Click "Create Transaction" to receive a payment link
4. Open the payment link in a new tab and complete the payment
5. Click "Check Payment Status" to verify the payment status
6. View the request log to see all requests and responses
7. Click "Copy Log" to copy the entire log
8. Click "Refresh Webhooks" to fetch webhooks
9. View the webhooks list in chronological order
10. Click "Copy Webhooks" to copy the entire list
11. Write test results in `1_result/3.test_page.md` as a new section "Test Results"

## Output Requirements

**Files to Create**:
1. `<integration_folder>/1_result/3.test_page.html` - The functional test page
2. `<integration_folder>/1_result/3.test_page.md` - Documentation with:
   - Embedded link to the HTML file
   - Instructions for using the test page
   - (If Phase 2 executed) Screenshots/Logs of successful transaction
   - (If Phase 2 executed) Test Results section

## Implementation Guidelines

### HTML Structure
- Single-file HTML with embedded CSS and JavaScript (no external dependencies except CORS proxy if needed)
- Use modern JavaScript (ES6+) with `async/await`
- Include proper error handling with user-friendly error messages
- Use `sessionStorage` for credential persistence
- Implement auto-polling for webhooks (5-second interval) with manual refresh option

### Design Principles
- Mobile-responsive layout
- Clear visual separation between sections (Credentials, Transaction, Logs, Webhooks)
- Use copy-to-clipboard functionality for logs and webhooks
- Display loading states for async operations
- Show timestamps in human-readable format

### Security Considerations
- Never hardcode credentials
- Use HTTPS endpoints when possible
- Validate all user inputs before making API requests
- Display sensitive data (like tokens) with option to show/hide

### Testing Checklist
Before marking this step complete, verify:
- [ ] Token generation works
- [ ] Transaction creation returns a payment link
- [ ] Payment link opens correctly
- [ ] Status check retrieves updated status
- [ ] Request log shows all API calls
- [ ] Webhook polling works automatically
- [ ] Webhook data displays correctly
- [ ] All copy buttons work
- [ ] Credentials persist in sessionStorage
- [ ] Page works in different browsers (Chrome, Firefox)

## Example Usage

User might say:
> "Execute Step 3 - create the local test page for this integration"

You should:
1. Read the integration's `integration_config` file.
2. Read the provider's API documentation
3. Generate `3.test_page.html` with all required functionality
4. Create `3.test_page.md` with usage instructions
5. If user requests, execute automated testing with browser tool

## Related Resources
- Example test page: `examples/sample_test_page.html`
- Webhook format reference: `resources/webhook_format.json`
- **Style Guide**: `resources/style_guide.md` (Contains mandatory CSS and Layout definitions)
