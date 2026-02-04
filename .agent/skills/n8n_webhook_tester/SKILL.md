---
name: N8n Webhook Tester
description: Test webhooks using n8n infrastructure with unique order IDs and automated polling
---

# N8n Webhook Tester Skill

## Overview

This skill provides infrastructure for testing payment provider webhooks using the n8n webhook testing service. It allows you to:
- Generate unique order IDs for each transaction
- Configure webhook URLs that the provider should call
- Retrieve and verify webhook payloads with automated polling
- Format webhook data for inclusion in reports

## When to Use This Skill

Use this skill when:
- **Step 2 (API Verification)**: Testing webhook callbacks during manual API verification
- **Step 4 (Automated Testing)**: Verifying webhooks in automated test page flows
- **Debugging**: Investigating webhook delivery issues
- **Documentation**: Capturing real webhook payloads for technical specifications

## Prerequisites

- Internet access to reach `https://n8n.4bill.io`
- The `requests` Python library (for programmatic usage)

## N8n Infrastructure Details

### Webhook Send Endpoint
**URL Pattern**: `https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b/:orderId`

This is the URL you provide to the payment provider as the webhook/callback URL. Replace `:orderId` with a unique identifier for each transaction.

**Example**:
```
https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b/a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

### Webhook Retrieve Endpoint
**URL Pattern**: `https://n8n.4bill.io/webhook/ea6540ee-da8f-499e-a2bb-92111e8fb689/:orderId`

This endpoint retrieves all webhooks received for a specific `orderId`.

**Authentication**: Basic Auth
- **Username**: `callbacks-test`
- **Password**: `callbacks-test123`

**Example Curl**:
```bash
curl -X GET "https://n8n.4bill.io/webhook/ea6540ee-da8f-499e-a2bb-92111e8fb689/a1b2c3d4-e5f6-7890-abcd-ef1234567890" \
  -u "callbacks-test:callbacks-test123"
```

## Usage Patterns

### Pattern 1: Manual Verification (Step 2)

**Scenario**: You're manually testing the API with curl commands and need to verify webhook delivery.

**Steps**:
1. **Generate a unique order ID**:
   ```bash
   python3 .agent/skills/n8n_webhook_tester/scripts/n8n_helper.py generate
   ```
   Output:
   ```
   Generated Order ID: a1b2c3d4-e5f6-7890-abcd-ef1234567890
   Send URL: https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b/a1b2c3d4-e5f6-7890-abcd-ef1234567890
   ```

2. **Use the Send URL in your transaction creation**:
   ```bash
   curl -X POST "https://api.provider.com/v1/transactions" \
     -H "Authorization: Bearer $TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "amount": 100.50,
       "currency": "USD",
       "callback_url": "https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b/a1b2c3d4-e5f6-7890-abcd-ef1234567890"
     }'
   ```

3. **Complete the payment** (if required by the provider flow)

4. **Retrieve the webhook**:
   ```bash
   curl -X GET "https://n8n.4bill.io/webhook/ea6540ee-da8f-499e-a2bb-92111e8fb689/a1b2c3d4-e5f6-7890-abcd-ef1234567890" \
     -u "callbacks-test:callbacks-test123"
   ```

5. **Document in report**: Include the webhook payload in your `2.docs_analysis.md`

### Pattern 2: Programmatic Usage (Step 4)

**Scenario**: You're automating webhook verification in the test page or Python scripts.

**Example**:
```python
from .agent.skills.n8n_webhook_tester.scripts.n8n_helper import N8nWebhookTester

# Generate unique order ID
order_id = N8nWebhookTester.generate_order_id()
print(f"Order ID: {order_id}")

# Get the webhook URL to send to the provider
webhook_url = N8nWebhookTester.get_send_url(order_id)
print(f"Webhook URL: {webhook_url}")

# ... create transaction with webhook_url ...

# Wait for and retrieve webhooks (with automatic polling)
try:
    webhooks = N8nWebhookTester.retrieve_webhooks(
        order_id=order_id,
        timeout=60,  # Wait up to 60 seconds
        poll_interval=5  # Check every 5 seconds
    )
    
    # Format for report
    report_section = N8nWebhookTester.format_for_report(webhooks)
    print(report_section)
    
except TimeoutError:
    print("No webhooks received within timeout period")
```

### Pattern 3: Test Page Integration

**Scenario**: Adding n8n webhook support to HTML test pages.

**JavaScript Example**:
```javascript
// Generate unique order ID (use UUID v4)
const orderId = crypto.randomUUID();

// Construct webhook URL
const webhookUrl = `https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b/${orderId}`;

// Use in transaction creation
const transactionData = {
    amount: 100.50,
    currency: "USD",
    callback_url: webhookUrl
};

// ... create transaction ...

// Poll for webhooks
async function pollWebhooks(orderId, maxAttempts = 12) {
    const retrieveUrl = `https://n8n.4bill.io/webhook/ea6540ee-da8f-499e-a2bb-92111e8fb689/${orderId}`;
    const auth = btoa('callbacks-test:callbacks-test123');
    
    for (let i = 0; i < maxAttempts; i++) {
        const response = await fetch(retrieveUrl, {
            headers: {
                'Authorization': `Basic ${auth}`
            }
        });
        
        if (response.ok) {
            const webhooks = await response.json();
            if (webhooks && webhooks.length > 0) {
                return webhooks;
            }
        }
        
        // Wait 5 seconds before next attempt
        await new Promise(resolve => setTimeout(resolve, 5000));
    }
    
    throw new Error('No webhooks received within timeout');
}

// Usage
try {
    const webhooks = await pollWebhooks(orderId);
    console.log('Received webhooks:', webhooks);
} catch (error) {
    console.error('Webhook polling failed:', error);
}
```

## Python Utility Reference

The `scripts/n8n_helper.py` provides a `N8nWebhookTester` class with the following methods:

### `generate_order_id() -> str`
Generates a unique UUID for use as an order ID.

### `get_send_url(order_id: str) -> str`
Returns the complete webhook URL for the provider to call.

### `retrieve_webhooks(order_id: str, timeout: int | None = None, poll_interval: int | None = None) -> list[dict]`
Polls the n8n endpoint and retrieves webhooks. Raises `TimeoutError` if no webhooks are received.

**Parameters**:
- `order_id`: The unique transaction identifier
- `timeout`: Maximum wait time in seconds (default: 60)
- `poll_interval`: Time between polling attempts (default: 5)

### `format_for_report(webhooks: list[dict]) -> str`
Formats webhook data as markdown for inclusion in reports.

### `get_curl_example(order_id: str) -> str`
Generates a ready-to-use curl command for manual testing.

## CLI Usage

The Python utility can also be used from the command line:

```bash
# Generate a new order ID
python3 .agent/skills/n8n_webhook_tester/scripts/n8n_helper.py generate

# Get send URL for an order ID
python3 .agent/skills/n8n_webhook_tester/scripts/n8n_helper.py send <order_id>

# Retrieve webhooks (with polling)
python3 .agent/skills/n8n_webhook_tester/scripts/n8n_helper.py retrieve <order_id>

# Get curl example
python3 .agent/skills/n8n_webhook_tester/scripts/n8n_helper.py curl <order_id>
```

## Configuration

Configuration is stored in `resources/config.json`:

```json
{
  "n8n_endpoints": {
    "send_webhook_base_url": "https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b",
    "retrieve_webhook_base_url": "https://n8n.4bill.io/webhook/ea6540ee-da8f-499e-a2bb-92111e8fb689"
  },
  "auth": {
    "username": "callbacks-test",
    "password": "callbacks-test123"
  },
  "defaults": {
    "timeout_seconds": 60,
    "poll_interval_seconds": 5,
    "max_retries": 12
  }
}
```

## Report Format Example

When documenting webhook verification in `2.docs_analysis.md`, use this format:

```markdown
## Webhook Verification (N8n)

**Order ID**: `a1b2c3d4-e5f6-7890-abcd-ef1234567890`
**Webhook URL**: `https://n8n.4bill.io/webhook/0154f998-9882-4b6b-b08b-a3a9e6e3d38b/a1b2c3d4-e5f6-7890-abcd-ef1234567890`

### Retrieval Command
\`\`\`bash
curl -X GET "https://n8n.4bill.io/webhook/ea6540ee-da8f-499e-a2bb-92111e8fb689/a1b2c3d4-e5f6-7890-abcd-ef1234567890" \\
  -u "callbacks-test:callbacks-test123"
\`\`\`

### Received Webhooks

**Total Webhooks Received**: 2

#### Webhook 1
\`\`\`json
{
  "transaction_id": "TXN123456",
  "status": "pending",
  "amount": 100.50,
  "currency": "USD",
  "timestamp": "2026-02-04T18:30:00Z"
}
\`\`\`

#### Webhook 2
\`\`\`json
{
  "transaction_id": "TXN123456",
  "status": "paid",
  "amount": 100.50,
  "currency": "USD",
  "timestamp": "2026-02-04T18:31:15Z"
}
\`\`\`

### Analysis
- Provider sends webhooks for both `pending` and `paid` statuses
- Webhook delivery time: ~75 seconds after transaction creation
- Payload includes transaction_id, status, amount, currency, and timestamp
```

## Troubleshooting

### No webhooks received
- **Check order ID**: Ensure you're using the exact same order ID for send and retrieve
- **Wait longer**: Some providers have delayed webhook delivery (30-60 seconds)
- **Verify callback URL**: Confirm the provider accepted the webhook URL in the transaction request
- **Check provider logs**: Some providers have webhook delivery logs in their dashboard

### Authentication errors
- Verify credentials in `resources/config.json`
- Ensure Basic Auth header is properly formatted: `Authorization: Basic base64(username:password)`

### Timeout errors
- Increase timeout parameter: `retrieve_webhooks(order_id, timeout=120)`
- Check if the provider requires manual payment completion
- Verify the provider's webhook configuration in their dashboard

## Best Practices

1. **Unique Order IDs**: Always generate a new order ID for each transaction to avoid confusion
2. **Document Everything**: Include the order ID, webhook URL, and retrieval command in your reports
3. **Wait Appropriately**: Some providers delay webhook delivery; use adequate timeout values
4. **Verify Signatures**: If the provider sends webhook signatures, document the verification method
5. **Test Multiple Scenarios**: Test webhooks for success, failure, and pending states

## Integration with Workflows

This skill is referenced in:
- **Step 2**: Documentation & API Verification workflow
- **Step 4**: Automated Test Page workflow
- **API Verification Report**: Webhook verification section
- **Test Page Generator**: Webhook testing functionality
