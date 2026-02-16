# Bank Transfer Payin HPP

**Bank Transfer** are a common payment method in Ecuador, with over 8 million users. Transfers are made in US dollars, and the process requires users to copy the recipient's account number and paste it into their banking app. If the entered amount differs from the expected transaction, the transfer still completes, and the merchant receives the actual amount sent.

[![Logo](/img/method_logos/ecuador/bank_transfer/darkmode.png)](https://docs.betterbro.com/downloads/method_logos/ecuador/bank_transfer.zip)

![](/icons/notification/info.svg)
You can find more information about this method and the video flow on our [Knowledge Hub](https://hub4merchant.notion.site/ecuador#1dfee5da506f809b8b0af07a3cbc6a0f) portal

## Payment flow
1. The customer on the merchant's website selects this method of payment
2. The merchant [creates a transaction](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#create-a-transaction) by calling the [/v2/transaction/create](https://docs.betterbro.com/api/v2/transaction/create) endpoint. In response to the request, the merchant will receive a `pay_url` to the payment page, to which it redirects the customer
3. On the payment page, the customer is shown payment details to make a bank transfer
4. The customer goes to the banking application by themselves and makes a transfer using the specified details
5. _*The customer returns to the payment page, confirms the transfer and provides their first and last name to speed up the transaction confirmation_
6. The merchant expects to receive a [callback](https://docs.betterbro.com/callbacks)

\* This step may be skipped in the payment flow, check with the **betterbro** manager for details

![](/icons/notification/info.svg)
The maximum lifetime of a transaction is 10 minutes  
The details are valid for 10 minutes

## Create a transaction
To create a transaction, use the [/v2/transaction/create](https://docs.betterbro.com/api/v2/transaction/create) endpoint.
Data exchange with the payment gateway API is performed exclusively in **JSON** format via the **POST** method.

### Authentication
Headers required:
- `X-Timestamp`: Unix timestamp (one-second precision).
- `X-Point-ID`: Identifier of the point (`point_id`).
- `X-Signature`: HMAC SHA256 signature calculated using the request body and the point's API token.

### Request Body Parameters
| Name | Type | Mandatory | Description |
| --- | --- | --- | --- |
| **locale** | string | Yes | Language code (e.g., `es`, `en`) |
| **external_customer_id** | string | Yes | Customer's ID in merchant system |
| **customer_ip_address** | string | Yes | Customer's IP address |
| **external_transaction_id** | string | Yes | Unique transaction ID in merchant system |
| **account_id** | integer | Yes | Merchant account ID |
| **wallet_id** | integer | Yes | Merchant wallet ID |
| **service_id** | integer | Yes | Payment gateway service ID |
| **amount** | integer | Yes | Amount multiplied by 100 (e.g., 500000 for 5000.00 USD) |
| **amount_currency** | string | Yes | `USD` |
| **point.callback_url** | string | No | URL for callback transmission |
| **point.return_url** | string | No | URL to redirect customer back |

### Request Body Parameters – fields
| Name | Type | Mandatory* | Description |
| --- | --- | --- | --- |
| **fields.first_name** | string | No | Customer's first name |
| **fields.last_name** | string | No | Customer's last name |
| **fields.phone** | string | No | Format: `+593XXXXXXXXX` |
| **fields.email** | string | No | Customer's email |
| **fields.tax_id_type** | string | No | `CI`, `RUC`, or `PASS` |
| **fields.tax_id** | string | No | Document number |
*\* If not provided in the request, the user must provide them on the HPP.*

### Request Body Example
```json
{
    "locale": "es",
    "external_customer_id": "123",
    "customer_ip_address": "166.139.8.122",
    "external_transaction_id": "1234567890",
    "account_id": 123,
    "wallet_id": 123,
    "service_id": 123,
    "description": "Test payment",
    "amount": 500000,
    "amount_currency": "USD",
    "point": {
        "callback_url": "https://your.server.callback.url",
        "return_url": "https://your.server.return.url"
    },
    "fields": {
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+593991234567",
        "email": "example@mail.com",
        "tax_id_type": "RUC",
        "tax_id": "1234567890001"
    }
}
```

### Transaction Statuses
- `0 (NEW)`: Transaction created.
- `10 (PENDING)`: Waiting for payment.
- `1 (SUCCESS)`: Final successful status.
- `2 (FAILED)`, `3 (CANCELLED)`, `5 (EXPIRED)`: Final unsuccessful statuses.
