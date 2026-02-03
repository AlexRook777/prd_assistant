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

**Step 1**: Create a test HTML page with a **Proxy Switcher**:
- The "API Credentials" card header must have a toggle switch on the right side labeled "Use Proxy".
- If enabled, all API requests (OAuth, Transaction, Status) must be routed through `http://localhost:8000/proxy`.
- If disabled, requests go directly to the provider's API.
- The page must allow the user to:
    - Enter all required credentials
    - Receive a payment link
    - Open the payment link in a new tab
    - Check payment status via a button
    - View updated payment status within the payment details on the page

**Step 2**: Add optional callback URL configuration. The page must include:
- Option to view and copy all requests and responses (including headers)
- Request log with individual entry copy functionality
- Button to copy the entire log (including URL, method, headers, body, and response)

**Step 3**: Design and Logic Requirements.
- **MANDATORY**: You **MUST** use the standard CSS and HTML structure definitions from `resources/style_guide.md`. Read this file before generating the HTML.
- **Proxy Logic**:
    - **Header Layout**: Use `<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;"><h2>API Credentials</h2><div class="switch-container">...</div></div>`.
    - **Persistence**: Save the switch state in `sessionStorage` (key: `use-proxy`).
    - **Request Format (Proxy ON)**:
        - URL: `http://localhost:8000/proxy`
        - Method: `POST`
        - Body: `JSON.stringify({ url: targetUrl, method: targetMethod, headers: targetHeaders, body: targetBody })`
    - **Response Handling (Proxy ON)**:
        - The proxy *always* returns 200 if the proxying succeeded.
        - The actual upstream response is in the JSON body: `{ status: <int>, headers: <dict>, body: <string|obj> }`.
        - **CRITICAL**: The `body` from the proxy might be a JSON **string** (serialized) or an object. You **MUST** check if `data.body` is a string and, if so, `JSON.parse()` it before using it.
        - You MUST unwrap this to treat it effectively as the real response (e.g., use `data.status` for success checks).
- **Robust Parsing**: Handle nested JSON responses (e.g., `data.data.access_token` vs `data.access_token`). Check multiple common paths for tokens and links.
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
- **Hardcode** the webhook URL to `http://localhost:8000/webhook`.
- **Hardcode** the polling endpoint to `http://localhost:8000/api/webhooks`.
- **EMBED THE WEBHOOK VIEWER UI**:
  - Do not just make a list. create a dedicated section that mimics the functionality of `serve.py`'s webhook viewer.
  - See `repos/prd_assistant/app/webhook_viewer.html` for reference on CSS and Logic.
  - It MUST include:
    - Auto-polling every 5 seconds.
    - "Refresh" and "Clear Logs" buttons (Clear logs via `DELETE /api/webhooks`).
    - Expandable details for Body and Headers.
    - Copy buttons.
- Display webhooks in chronological order (newest first).
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
