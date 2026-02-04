---
name: API Verification Report
description: Perform deep-dive API verification including active curl testing, validation of error cases, and discrepancy reporting.
---

# API Verification & Reporting Skill

This skill guides you through creating a high-quality API verification report (`2.docs_analysis.md`) by actively testing the provider's API against its documentation.

## Goal
To produce a comprehensive report that not only analyzes the static documentation but **Proves** how the API works by executing real requests and analyzing the differences.

## Prerequisites
-   You typically need `clientId`, `clientSecret` (or similar credentials) available in the workspace `integration_config`.
-   You must be able to reach the Sandbox environment via `curl`.

## Execution Steps

### 1. Static Documentation Analysis (Comprehensive Research)
-   **Action**: Read the documentation to understand the theoretical flow and extract all critical integration details.
-   **Extract and Document**:
    -   **Authentication Method**:
        -   Type (OAuth 2.0, API Key, Basic Auth, etc.)
        -   Token endpoint URL and required credentials
        -   Token lifetime and refresh mechanism
        -   Required headers for authenticated requests
    -   **Transaction Initiation**:
        -   Correct API endpoint URL for transaction creation
        -   HTTP method (POST, PUT, etc.)
        -   Request format (JSON, form-urlencoded, etc.)
    -   **Expected Results**:
        -   Response structure and HTTP status codes
        -   Transaction ID format and location in response
        -   Any redirect URLs or next steps
    -   **Data Structure** (Transaction Request):
        -   **Mandatory fields**: Required parameters with types and formats
        -   **Optional fields**: Parameters that can be omitted or have defaults
        -   Field validation rules and constraints
        -   Nested object structures (customer, billing, shipping, etc.)
    -   **Payment URL Response**:
        -   Where in the response is the payment/checkout URL?
        -   URL format and structure
        -   URL lifetime and expiration rules
    -   **Callbacks (Webhooks)**:
        -   Webhook endpoint configuration location
        -   Callback payload structure and fields
        -   Authentication/signature verification method
        -   Retry policy and failure handling
    -   **Status Sets**:
        -   Complete list of all possible transaction statuses
        -   Status transitions and flow diagram
        -   Final states (success, failure, cancelled, etc.)
        -   Intermediate or pending states
-   **Clarify**: Note any specific "Clarified Points" or user constraints (e.g., "Chile only", "HPP only").

### 2. Active Authentication (The "Hello World")
-   **Action**: Construct and run a `curl` command to get an access token.
-   **Verify**: 
    -   Does it require specific headers?
    -   Does it answer 200 OK?
-   **Output**: Capture the *exact* request and response.

### 3. Transaction "Happy Path"
-   **Action**: Create a *valid* transaction using `curl`.
    -   Use dummy data (e.g., `customer.email="test@example.com"`).
    -   Ensure all "Required" fields from docs are present.
-   **Verify**:
    -   Does it return `200 OK` / `201 Created`?
    -   **CRITICAL**: Immediately check the status (GET /transaction/{id}). Does it match?

### 4. "Negative Testing" (Validation Rules)
Run at least **3 specific failure scenarios** to find real error codes:
1.  **Missing Required Field**: e.g., omit `customer.name`.
2.  **Invalid Data Type**: e.g., send `amount` as string `"100.00"` instead of number.
3.  **Business Logic Error**: e.g., `amount: -100`.

### 5. Webhook Verification (N8n)
-   **Action**: Test webhook delivery using the n8n webhook testing infrastructure.
-   **Steps**:
    1.  Generate a unique order ID using the **N8n Webhook Tester** skill (`.agent/skills/n8n_webhook_tester/SKILL.md`).
    2.  Construct the webhook URL: `https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b/{orderId}`
    3.  Create a transaction with this webhook URL as the callback/notification URL.
    4.  Complete the payment flow (if required by the provider).
    5.  Poll for webhooks using: `curl -X GET "https://n8n.4bill.io/webhook/ea6540ee-da8f-499e-a2bb-92111e8fb689/{orderId}" -u "callbacks-test:callbacks-test123"`
    6.  Document the received webhook payload(s) in the report.
-   **Note**: See the N8n Webhook Tester skill for detailed usage patterns and examples.

### 6. Discrepancy & Gap Analysis
Compare Doc Theory vs API Reality.
-   Did the API require a field listed as optional?
-   Did the API return a String where Int was promised?

## Report Output Format

Generates a report (filename specified by the caller) with the following structure:

```markdown
# Documentation Analysis

**Provider**: [Provider Name]
**Documentation URL**: [URL]
**Date**: [YYYY-MM-DD]

## Clarified Points (User Feedback)
- [List any specific constraints or user clarifications found in previous steps or provided context]

## Authentication
### Method
[e.g., OAuth 2.0 with Bearer Token / API Key / Basic Auth]
### Token Generation
- **Endpoint**: \`POST https://...\`
- **Required Headers**: \`Content-Type: application/x-www-form-urlencoded\`
- **Required Credentials**: \`client_id\`, \`client_secret\`
- **Token Lifetime**: [e.g., 3600 seconds]
- **Refresh Mechanism**: [How to refresh expired tokens]
### Verification (MANDATORY)
Successfully verified. Obtained token using:
\`\`\`bash
[CURL COMMAND]
\`\`\`

## Transaction Initiation
### Create Transaction Endpoint
- **Endpoint**: \`POST https://api.provider.com/v1/transactions\`
- **HTTP Method**: POST
- **Request Format**: application/json
- **Authentication**: Bearer Token in Authorization header

### Data Structure
#### Mandatory Fields
| Field | Type | Format | Description | Example |
|-------|------|--------|-------------|---------|
| \`amount\` | number | Decimal(10,2) | Transaction amount | 100.50 |
| \`currency\` | string | ISO 4217 | Currency code | "USD" |
| \`customer.email\` | string | Email | Customer email | "user@example.com" |

#### Optional Fields
| Field | Type | Format | Description | Default |
|-------|------|--------|-------------|---------|
| \`description\` | string | Max 255 chars | Transaction description | null |
| \`customer.phone\` | string | E.164 | Customer phone | null |

#### Nested Structures
- **customer**: Object containing customer information
  - \`name\` (string, required)
  - \`email\` (string, required)
  - \`phone\` (string, optional)
- **billing**: Object containing billing address (optional)

### Expected Results
- **Success Status Code**: 201 Created
- **Response Structure**:
\`\`\`json
{
  "transaction_id": "TXN123456",
  "status": "pending",
  "payment_url": "https://checkout.provider.com/pay/ABC123"
}
\`\`\`
- **Transaction ID Format**: [e.g., Alphanumeric, 8-16 characters]
- **Transaction ID Location**: \`response.transaction_id\`

## Payment URL Response
- **URL Location**: \`response.payment_url\` or \`response.checkout_url\`
- **URL Format**: \`https://checkout.provider.com/pay/{token}\`
- **URL Lifetime**: [e.g., 24 hours, 7 days, or "Does not expire"]
- **Redirect Behavior**: [e.g., User completes payment and returns to success_url]

## Status Sets
### Complete Status List
| Status | Description | Type | Next Possible States |
|--------|-------------|------|---------------------|
| \`pending\` | Transaction created, awaiting payment | Intermediate | paid, cancelled, expired |
| \`paid\` | Payment successful | Final | - |
| \`failed\` | Payment failed | Final | - |
| \`cancelled\` | Transaction cancelled | Final | - |
| \`expired\` | Payment URL expired | Final | - |

### Status Flow
\`\`\`
pending → paid (success)
pending → failed (payment declined)
pending → cancelled (user/merchant action)
pending → expired (timeout)
\`\`\`

## API Endpoints
### Check Status
- **Endpoint**: \`GET https://api.provider.com/v1/transactions/{id}\`
- **Authentication**: Bearer Token

### Webhook Callback
- **Format**: POST to merchant-provided URL
- **Authentication**: HMAC-SHA256 signature in \`X-Signature\` header
- **Secret Location**: Provider dashboard → Settings → Webhooks
- **Payload Structure**:
\`\`\`json
{
  "transaction_id": "TXN123456",
  "status": "paid",
  "amount": 100.50,
  "currency": "USD"
}
\`\`\`
- **Retry Policy**: [e.g., 3 retries with exponential backoff]
- **Failure Handling**: [e.g., Manual retry from dashboard]

## Verification Part
### Successful Transaction (Happy Path)
\`\`\`bash
[CURL COMMAND defined in Step 3]
\`\`\`
**Response**:
\`\`\`json
[REAL JSON RESPONSE]
\`\`\`

## Live Payment Link (Verification)

**Generated**: [YYYY-MM-DD HH:MM:SS UTC]
**Transaction ID**: [e.g., TXN123456789]
**Payment URL**: [e.g., https://checkout.provider.com/pay/abc123def456]
**Expires**: [e.g., 2026-02-05 14:22:00 UTC (24 hours) or "Does not expire"]

### Testing Instructions
1. Open the payment URL in a browser
2. Complete the payment flow using test card credentials from provider documentation
3. Verify the redirect to success/failure URL
4. Check webhook callback reception (if configured)
5. Verify transaction status update via GET endpoint

**Note**: This live payment link proves that the integration successfully creates transactions and generates functional payment URLs.

## Webhook Verification (N8n)

**Order ID**: `[Generated UUID]`
**Webhook URL**: `https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b/[orderId]`
**Retrieval Endpoint**: `https://n8n.4bill.io/webhook/ea6540ee-da8f-499e-a2bb-92111e8fb689/[orderId]`

### Retrieval Command
\`\`\`bash
curl -X GET "https://n8n.4bill.io/webhook/ea6540ee-da8f-499e-a2bb-92111e8fb689/[orderId]" \\
  -u "callbacks-test:callbacks-test123"
\`\`\`

### Received Webhooks

**Total Webhooks Received**: [Number]

#### Webhook 1
\`\`\`json
[ACTUAL WEBHOOK PAYLOAD]
\`\`\`

### Webhook Analysis
- **Delivery Time**: [Time from transaction creation to webhook receipt]
- **Status Updates**: [List of statuses received via webhook]
- **Payload Structure**: [Description of webhook payload fields]
- **Authentication**: [How the provider signs/authenticates webhooks, if applicable]

### Negative Testing (Validation)
| Test Case    | Variation     | Expected | Actual Code | JSON Error        |
| ------------ | ------------- | -------- | ----------- | ----------------- |
| Missing Name | Omit Name     | 400      | 422         | \`{"error":...}\` |
| Bad Type     | String Amount | 400      | 200         | (Accepted)        |

## Gap Analysis (Discrepancies)
| #   | Issue       | Documentation | Actual Behavior      | Severity |
| --- | ----------- | ------------- | -------------------- | -------- |
| 1   | Amount Type | Integer       | String               | Low      |
| 2   | Email       | Optional      | Required (500 Error) | High     |

## Questions for Provider
- [Specific technical questions]
```
