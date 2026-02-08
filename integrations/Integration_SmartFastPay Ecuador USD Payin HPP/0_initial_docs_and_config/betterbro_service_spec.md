# Bank Transfer Payin HPP (Ecuador) - BetterBro Specification

**Service URL**: `https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp`

## 1. Request Parameters (Standard Fields)

| Name | Type | Mandatory | Description |
| --- | --- | --- | --- |
| **locale** | string | Yes | `es` or `en` |
| **external_customer_id** | string | Yes | Customer ID in merchant system |
| **customer_ip_address** | string | Yes | Required for anti-fraud |
| **external_transaction_id** | string | Yes | Unique Transaction ID |
| **account_id** | integer | Yes | Provided by manager |
| **wallet_id** | integer | Yes | Provided by manager |
| **service_id** | integer | Yes | Provided by manager |
| **amount** | integer | Yes | Amount * 100 |
| **amount_currency** | string | Yes | `USD` |
| **point.callback_url** | string | No | Webhook URL |
| **point.return_url** | string | No | Redirect URL |

## 2. Customer Fields (`fields` object)

| Name | Mandatory | Description |
| --- | --- | --- |
| **first_name** | No* | At least one word, 2+ letters |
| **last_name** | No* | At least one word, 2+ letters |
| **phone** | No* | International format (+593XXXXXXXXX) |
| **email** | No* | Valid email |
| **tax_id_type** | No* | `CI` (National ID), `RUC`, `PASS` |
| **tax_id** | No* | Up to 10 digits for CI, 13 for RUC |

\* If not provided, user must fill on checkout page.

## 3. Standard Statuses (Rosetta)

| Code | Status | Description |
| --- | --- | --- |
| 1 | SUCCESS | Final success |
| 2 | FAILED | Final failure |
| 3 | CANCELLED | Final cancellation |
| 5 | EXPIRED | Request time limit exceeded |
| 10 | PENDING | Awaiting payment/confirmation |
