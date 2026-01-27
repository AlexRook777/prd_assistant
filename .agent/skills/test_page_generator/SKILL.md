---
name: Test Page Generator
description: Generate functional HTML test pages for payment provider API verification with webhook testing support
---

# Test Page Generator Skill

## When to Use This Skill
Automatically activate when user mentions:
- "create test page" or "generate test page"
- "Step 3" or "local test page" in research context
- Testing payment provider APIs
- HPP (Hosted Payment Page) testing

This skill is specifically designed for **Phase 1, Step 3** of the integration workflow.

## Prerequisites
The following must be configured in the integration's `config` file:
- `PROVIDER_API_DOCUMENTATION_URL`: Link to the provider's API documentation
- `TEST_POST_WEBHOOK_URL`: Universal webhook test URL (format: `https://webhook.site/unique-uuid-{orderId}`)
- `TEST_GET_WEBHOOK_URL`: URL to retrieve webhooks via GET request (protected by Basic Auth)

## Task Description

### Phase 1: Create Test Page

**Step 1**: Create a test HTML page where the user can:
- Enter all required credentials (from the provider's documentation)
- Receive a payment link
- Open the payment link in a new tab
- Check payment status via a button
- View updated payment status within the payment details on the page

**Step 2**: Add optional callback URL configuration. The page must include:
- Option to view and copy all requests and responses (including headers)
- Request log with individual entry copy functionality
- Button to copy the entire log (including URL, method, headers, body, and response)

**Step 3**: Design the page to be professional and user-friendly. However, **functional correctness and flexibility** in configuring request parameters is the main priority. 
- Save all entered credentials in `sessionStorage` so they persist on page reload
- Clear credentials when the browser is closed
- Use a clean, modern design with proper form validation

**Step 4**: Webhook Verification
- Use the universal test URL from config: `{TEST_POST_WEBHOOK_URL}` where `orderId` is substituted dynamically and uniquely for each transaction
- To retrieve webhooks, use GET request to `{TEST_GET_WEBHOOK_URL}` (protected by Basic Auth)
- User will enter the Basic Auth username and password in the form before creating a transaction
- After transaction creation, automatically fetch processed webhooks every 5 seconds
- Display webhooks in chronological order in the interface
- Add a manual refresh button
- Expected webhook response format:
  ```json
  [
    {
      "_id": "694b97fc8faa2c4927f343f3",
      "callbackRawData": {
        "headers": {},
        "query": {},
        "body": {}
      },
      "timestamp": "2025-12-24T07:36:28.893Z",
      "timestampEpoch": 1766561788893,
      "callbackId": "orderId"
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
11. Write test results in `1_research/3.local_test_page.md` as a new section "Test Results"

## Output Requirements

**Files to Create**:
1. `<integration_folder>/1_research/3.test_page.html` - The functional test page
2. `<integration_folder>/1_research/3.local_test_page.md` - Documentation with:
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
1. Read the integration's `config` file. If `TEST_POST_WEBHOOK_URL` or `TEST_GET_WEBHOOK_URL` are missing, read them from `global_config` in the root directory.
2. Read the provider's API documentation
3. Generate `3.test_page.html` with all required functionality
4. Create `3.local_test_page.md` with usage instructions
5. If user requests, execute automated testing with browser tool

## Related Resources
- Example test page: `examples/sample_test_page.html`
- Webhook format reference: `resources/webhook_format.json`
