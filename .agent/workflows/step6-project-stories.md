---
description: Phase 1 Step 6 - Fill technical specifications for all project stories
---

# Step 6: Fill Project Stories

Create comprehensive technical specifications for all integration stories.

## Working Directory
`<current_integration>/1_research/`

## Output File
`6.project_stories.md`

## Task

1. **Pre-computation Check (CRITICAL)**:
   - Check if `6.project_stories.md` already exists.
   - **IF IT EXISTS**:
     - Read the file content.
     - Extract **Acceptance Criteria** status (checked/unchecked boxes).
     - **Preserve** any completed criteria in the new stories.
   - **IF IT DOES NOT EXIST**: Proceed normally.

2. Compile all technical details from previous steps into complete user stories.

```markdown
# Project Stories

**Integration**: [Provider Name]  
**Date**: [Current Date]

## Story 1: Authorization

### Description
Implement authentication mechanism for provider API access.

### Method
[OAuth 2.0 Client Credentials / API Key / HMAC Signature]

### Implementation Details
**Endpoint**: `POST /auth/token`

**Request Headers**:
```http
Authorization: Basic <base64(client_id:client_secret)>
Content-Type: application/json
```

**Request Body**:
```json
{
  "grant_type": "client_credentials"
}
```

**Response**:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

**Token Usage**:
All subsequent requests must include:
```http
Authorization: Bearer {access_token}
```

### Acceptance Criteria
- [ ] Token generation successful
- [ ] Token used in subsequent requests
- [ ] Token refresh logic implemented (if applicable)

---

## Story 2: Create Transaction Request

### Description
Create payment transaction and receive payment link or redirect URL.

### Endpoint
`POST /api/v1/transactions`

### Field Mapping

| BetterBro Field | Provider Field | Transformation | Example |
|-----------------|----------------|----------------|---------|
| `customer.email` | `email` | None | `user@example.com` |
| `customer.phone` | `phone` | E.164 format | `+593991234567` |
| `customer.document_id` | `document_id` | None | `1234567890` |
| `transaction.amount` | `amount` | Multiply by 100 | `1000` (for $10.00) |
| `transaction.currency` | `currency` | ISO 4217 | `USD` |
| `callback_url` | `webhook_url` | None | `https://api.betterbro.com/webhook` |

### Request Example
```json
{
  "amount": 1000,
  "currency": "USD",
  "email": "user@example.com",
  "phone": "+593991234567",
  "document_id": "1234567890",
  "webhook_url": "https://api.betterbro.com/webhook/{orderId}",
  "return_url": "https://example.com/return"
}
```

### Response Example (Success)
```json
{
  "transaction_id": "TXN_67890",
  "status": "pending",
  "payment_url": "https://provider.com/pay/abc123",
  "expires_at": "2025-01-23T15:00:00Z"
}
```

### Response Example (Error)
```json
{
  "error": "invalid_phone",
  "message": "Phone number must be in E.164 format"
}
```

### Acceptance Criteria
- [ ] All required fields mapped correctly
- [ ] Transaction created successfully
- [ ] Payment URL returned
- [ ] Error handling implemented

---

## Story 3: Create Transaction Response Parsing

### Description
Parse provider response and extract necessary information.

### Success Response Fields
| Field | Type | Purpose |
|-------|------|---------|
| `transaction_id` | string | Provider's transaction identifier |
| `status` | string | Current transaction status |
| `payment_url` | string | URL to redirect customer |
| `expires_at` | datetime | Payment URL expiration |

### Error Response Fields
| Field | Type | Purpose |
|-------|------|---------|
| `error` | string | Error code |
| `message` | string | Human-readable error message |

### Status Codes
| HTTP Code | Meaning | Action |
|-----------|---------|--------|
| 200 | Success | Proceed with payment URL |
| 400 | Bad Request | Log error, return to user |
| 401 | Unauthorized | Refresh token, retry |
| 500 | Server Error | Retry with exponential backoff |

---

## Story 4: Callback (Webhook)

### Description
Handle async notifications from provider about transaction status updates.

### Webhook Endpoint
Provider will POST to: `https://api.betterbro.com/webhook/{orderId}`

### Webhook Payload Example
```json
{
  "transaction_id": "TXN_67890",
  "status": "success",
  "amount": 1000,
  "currency": "USD",
  "timestamp": "2025-01-23T14:30:00Z",
  "signature": "abc123def456"
}
```

### Validation Logic
1. **Signature Verification**:
   ```
   HMAC-SHA256(payload, secret_key) == signature
   ```
2. **Timestamp Check**: Reject if older than 5 minutes
3. **Idempotency**: Check if already processed

### Response
Always return `200 OK` to acknowledge receipt:
```json
{
  "received": true
}
```

### Acceptance Criteria
- [ ] Webhook signature validated
- [ ] Transaction status updated
- [ ] Idempotency ensured
- [ ] 200 OK response sent

---

## Story 5: Check Status

### Description
Manually poll transaction status (fallback if webhook fails).

### Endpoint
`GET /api/v1/transactions/{transaction_id}`

### Response Example
```json
{
  "transaction_id": "TXN_67890",
  "status": "success",
  "amount": 1000,
  "created_at": "2025-01-23T14:00:00Z",
  "completed_at": "2025-01-23T14:30:00Z"
}
```

### Polling Strategy
- Poll every 5 seconds for first minute
- Then every 30 seconds for next 5 minutes
- Then every 5 minutes until timeout (30 min)

---

## Story 6: Final Statuses Mapping

### Description
Map provider statuses to internal BetterBro statuses.

| Provider Status | Internal Status | Meaning |
|----------------|-----------------|---------|
| `pending` | `PENDING` | Awaiting payment |
| `processing` | `PENDING` | Payment being processed |
| `success` | `SUCCESS` | Payment completed |
| `completed` | `SUCCESS` | Payment completed |
| `failed` | `FAILED` | Payment failed |
| `error` | `FAILED` | Technical error |
| `cancelled` | `CANCELLED` | User cancelled |
| `expired` | `EXPIRED` | Payment link expired |

---

## Story 7: Error Mapping

### Description
Map provider error codes to user-friendly messages.

| Provider Error Code | Internal Code | User Message |
|--------------------|---------------|--------------|
| `invalid_phone` | `INVALID_PHONE` | "Please enter a valid phone number" |
| `invalid_amount` | `INVALID_AMOUNT` | "Amount must be between $1 and $10,000" |
| `insufficient_funds` | `PAYMENT_FAILED` | "Insufficient funds" |
| `card_declined` | `PAYMENT_FAILED` | "Card declined by issuer" |
| `expired_card` | `PAYMENT_FAILED` | "Card has expired" |
| `network_error` | `TECHNICAL_ERROR` | "Technical error, please try again" |

---

## Next Steps
- [ ] Proceed to Step 7 (Field Testing)
```

## Success Criteria
- All 7 stories filled with complete technical details
- Field mappings documented
- Error handling specified
- Status mappings defined

## User Confirmation
- "Project Stories filled. Review `6.project_stories.md`. Should I proceed to Step 7 (Field Testing), or do you want to refine this step?"



