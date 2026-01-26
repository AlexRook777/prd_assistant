---
description: Phase 1 Step 2 - Analyze provider's API documentation
---

# Step 2: Documentation Analysis

Perform a deep dive into the payment provider's API documentation to understand authentication, endpoints, and payment flows.

## Working Directory
`<current_integration>/1_research/`

## Output File
`2.docs_analysis.md`

## Prerequisites
- `config` file must have `PROVIDER_API_DOCUMENTATION_URL` filled in

## Task

1. **Read Provider Documentation**:
   - Open and review the provider's API documentation from the URL in `config`
   - Also check `0_initial_docs/` for any downloaded documentation PDFs

2. **Authentication Analysis**:
   - Identify authentication method (API Key, OAuth, JWT, HMAC signature, etc.)
   - Document required headers
   - Note token generation process if applicable

3. **API Endpoints Inventory**:
   - List all relevant endpoints (create transaction, check status, webhooks)
   - Document HTTP methods (POST, GET, PUT)
   - Note required and optional parameters

4. **Payment Method Codes**:
   - Extract payment method identifiers
   - Document any country or currency restrictions per method

5. **Webhook Structure**:
   - Document callback URL format
   - Identify webhook authentication/validation method
   - Note expected response acknowledgment

6. **Customer Fields**:
   - List required customer fields (name, email, phone, document ID, etc.)
   - Document field formats and validation rules

7. **Create Documentation**:

```markdown
# Documentation Analysis

**Provider**: [Provider Name]  
**Documentation URL**: [Link from config]  
**Date**: [Current Date]

## Authentication

### Method
[API Key / OAuth 2.0 / JWT / HMAC / Basic Auth]

### Token Generation
- **Endpoint**: `[POST /auth/token]`
- **Required Headers**: 
  - `Authorization: Basic <base64(client_id:client_secret)>`
- **Request Body**:
  ```json
  {
    "grant_type": "client_credentials"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "eyJhbGc...",
    "expires_in": 3600
  }
  ```

## API Endpoints

### Create Transaction
- **Endpoint**: `[POST /api/v1/transactions]`
- **Authentication**: [Bearer Token]
- **Required Parameters**:
  - `amount` (integer, cents)
  - `currency` (string, ISO 4217)
  - `customer.email` (string)
  - [etc.]

### Check Status
- **Endpoint**: `[GET /api/v1/transactions/{id}]`
- **Authentication**: [Bearer Token]
- **Response Statuses**: [pending, success, failed, etc.]

### Webhook Callback
- **Expected Format**: POST to our callback URL
- **Authentication**: [Signature in header / HMAC / IP whitelist]
- **Payload Structure**:
  ```json
  {
    "transaction_id": "...",
    "status": "success",
    "timestamp": "..."
  }
  ```

## Payment Methods

| Method Code | Description | Countries | Currencies |
|-------------|-------------|-----------|------------|
| `wallet` | Digital wallet | EC | USD |
| [etc.] | | | |

## Required Customer Fields

| Field | Format | Required | Example |
|-------|--------|----------|---------|
| `email` | Email | Yes | `user@example.com` |
| `phone` | E.164 | No | `+593991234567` |
| `document_id` | Alphanumeric | Yes | `1234567890` |

## Restrictions & Quirks
- [Any unusual requirements]
- [Rate limits]
- [Sandbox vs Production differences]

## Questions / Gaps
- [Any unclear documentation]
- [Missing information]

## Next Steps
- [ ] Proceed to Step 3 (Local Test Page)
```

## Success Criteria
- File `2.docs_analysis.md` created with all sections filled
- All key endpoints documented with examples
- Authentication flow clearly described
- Customer fields table complete

## User Confirmation
After creating the file, ask:
- "Documentation Analysis complete. Review `2.docs_analysis.md`. Should I proceed to Step 3 (Local Test Page), or refine this step?"
