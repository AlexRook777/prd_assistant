---
description: Phase 1 Step 3 - Create functional HTML test page for API verification
---

# Step 3: Local Test Page

Create a functional HTML test page to physically verify the payment provider's API behavior and test webhooks.

## Working Directory
`<current_integration>/1_research/`

## Output Files
- `3.test_page.html` - Functional test page
- `3.local_test_page.md` - Documentation and test results

## Prerequisites
- `config` file must have:
  - `PROVIDER_API_DOCUMENTATION_URL`
  - `TEST_POST_WEBHOOK_URL`
  - `TEST_GET_WEBHOOK_URL`

## Task

1. **Pre-computation Check (CRITICAL)**:
   - Check if `3.local_test_page.md` already exists.
   - **IF IT EXISTS**:
     - Read the file content.
     - Extract **Test Results** (Token status, Transaction IDs, Screenshots).
     - Extract **Issues Found**.
     - **Preserve** these details in the new report.
   - **IF IT DOES NOT EXIST**: Proceed normally.

2. This step **automatically invokes** the `test_page_generator` skill. The skill will:

1. Read the provider's API documentation
2. Read the `config` file for webhook URLs and API details
3. Generate a functional HTML test page (`3.test_page.html`)
4. Create documentation (`3.local_test_page.md`)

### What the Test Page Must Include

**Core Functionality**:
- Credential input form (API keys, secrets, endpoints)
- Token generation (if required)
- Transaction creation with payment link
- Open payment link in new tab
- Check payment status button
- Display transaction details

**Webhook Testing**:
- Automatic webhook polling (every 5 seconds)
- Manual webhook refresh button
- Display webhooks in chronological order
- Copy individual webhooks and full log

**Request/Response Logging**:
- Show all API requests (URL, method, headers, body)
- Show all API responses
- Copy individual log entries
- Copy entire log

**User Experience**:
- Save credentials to `sessionStorage` (persist on reload)
- Professional, clean design
- Clear error messages
- Loading states for async operations

### Documentation Template

The skill will generate `3.local_test_page.md`:

```markdown
# Local Test Page

**Integration**: [Provider Name]  
**Date**: [Current Date]

## Test Page Location
[3.test_page.html](file:///absolute/path/to/3.test_page.html)

## Usage Instructions

### 1. Open the Test Page
Open `3.test_page.html` in your browser (Chrome or Firefox recommended).

### 2. Enter Credentials
Fill in the following fields from the `config` file:
- **Client ID**: [from config]
- **Client Secret**: [from config]
- **API Endpoint**: [from config]
- **Webhook Username**: [for Basic Auth]
- **Webhook Password**: [for Basic Auth]

### 3. Generate Token (if required)
Click "Get Token" to authenticate with the provider's API.

### 4. Create Transaction
Click "Create Transaction" to receive a payment link.

### 5. Complete Payment
Open the payment link in a new tab and complete the test payment.

### 6. Verify Status
Click "Check Payment Status" to see the updated status.

### 7. Review Webhooks
The page will automatically poll for webhooks every 5 seconds. Review the received webhook data.

## Test Results

### Token Generation
- **Status**: [Success/Failed]
- **Token**: `[redacted]`
- **Expires In**: [3600 seconds]

### Transaction Creation
- **Status**: [Success/Failed]
- **Transaction ID**: `[TXN_12345]`
- **Payment Link**: [URL]
- **Amount**: [10.00 USD]

### Payment Status
- **Initial Status**: `pending`
- **Final Status**: `success`
- **Timestamp**: [2025-01-23 14:00:00]

### Webhook Verification
- **Webhook Received**: [Yes/No]
- **Callback ID**: `[orderId]`
- **Payload**:
  ```json
  {
    "status": "success",
    "transaction_id": "TXN_12345"
  }
  ```

### Screenshots
[If browser tool used, embed screenshots here]

## Issues Found
- [List any issues or discrepancies]
- [Document any API quirks]

## Next Steps
- [ ] Proceed to Step 4 (Access & Field Verification)
```

## Success Criteria
- `3.test_page.html` created and functional
- `3.local_test_page.md` created with usage instructions
- If automated testing performed, test results documented
- Screenshots/logs included if available

## User Confirmation
After creating files, ask:
- "Local Test Page created and transaction verified. Review `3.local_test_page.md` and `3.test_page.html`. Should I proceed to Step 4 (Access & Fields), or do you want to refine this step?"



