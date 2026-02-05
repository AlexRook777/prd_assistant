# Bank Transfer Payin HPP

**Bank Transfer** are a common payment method in Ecuador, with over 8 million users. Transfers are made in US dollars, and the process requires users to copy the recipient's account number and paste it into their banking app. If the entered amount differs from the expected transaction, the transfer still completes, and the merchant receives the actual amount sent.

## Payment flow

1.  The customer on the merchant's website selects this method of payment
2.  The merchant creates a transaction by calling the /v2/transaction/create endpoint. In response to the request, the merchant will receive a `pay_url` to the payment page, to which it redirects the customer
3.  On the payment page, the customer is shown payment details to make a bank transfer
4.  The customer goes to the banking application by themselves and makes a transfer using the specified details
5.  *The customer returns to the payment page, confirms the transfer and provides their first and last name to speed up the transaction confirmation
6.  The merchant expects to receive a callback

* This step may be skipped in the payment flow, check with the betterbro manager for details

The maximum lifetime of a transaction is 10 minutes  
The details are valid for 10 minutes

## Create a transaction

To create a transaction, use the /v2/transaction/create endpoint.

Data exchange with the payment gateway API is performed exclusively in JSON format via the POST method. Each request must include the Content-Type: application/json header; otherwise, it will be considered invalid, even if the body contains valid JSON.

### Authentication

To successfully authenticate, all requests must contain valid JSON and include the following headers:

| Header | Description |
| --- | --- |
| X-Timestamp | Current timestamp generated directly before sending the request Format: Unix timestamp with one-second precision  Example: `1766129276` During request processing, it is verified that the current time does not exceed the X-Timestamp value by more than 60 seconds. If this condition is not met, the request will be rejected with 10 BAD_REQUEST error and the message: The request is out of date |
| X-Point-ID | Identifier of the point from which the request originates (`point_id`). It is used to determine the point's API token, which is required to verify the X-Signature Example: `556` |
| X-Signature | The cryptographic signature is calculated using the HMAC SHA256 hashing algorithm. For validation, the payment gateway recalculates the signature using the request body and the point's API token. If the values do not match, the request is rejected with error code 11 INVALID_AUTH Example: `d96180fe66442b2d0bf458e8a33e6e6d7867546ce136432c79afbf9e0297ee2a` |

### Request body parameters

| Name | Type | Mandatory | Max. length | Description |
| --- | --- | --- | --- | --- |
| **locale** | string | Yes | 2 | Language of the payment page Format: language code in the ISO 639-1 standard  Examples: `es` – Spanish, `en` – English |
| **external_customer_id** | string | Yes | 45 | Customer's ID in the merchant's system. Used for improvement of the transaction's search during incidents analysis, as well as for the operation of the anti-fraud system. If such parameter is absent in the system, it is necessary to send an alternative value for payer's identification, for example: mobile phone number or email |
| **customer_ip_address** | string | Yes | 39 | Customer's IP address. Both IPv4 and IPv6 addresses are allowed. It is important to send the customer's real IP to avoid false positives in the anti-fraud system |
| **external_transaction_id** | string | Yes | 128 | Transaction ID in the merchant system. Must be unique for each transaction. If a transaction already exists with the same `point_id` and `external_transaction_id`, payment creation will be rejected with an error 203 |
| **external_order_id** | string | No | 48 | Order ID in the merchant system. It is allowed to create multiple transactions with the same `external_order_id` |
| **account_id** | integer | Yes | — | Merchant account ID in the payment gateway. Provided by the betterbro manager |
| **wallet_id** | integer | Yes | — | Merchant wallet ID in the payment gateway. Provided by the betterbro manager |
| **service_id** | integer | Yes | — | Payment gateway service ID. Provided by the betterbro manager |
| **description** | string | No | 100 | Description of payment purpose |
| **amount** | integer | Yes | — | Payment amount multiplied by 100 Format: positive integer without decimals  Examples:  `5000.00 USD` is transmitted as `500000` (5000.00 x 100 = 500000)  `1534.20 USD` is transmitted as `153420` (1534.20 x 100 = 153420) |
| **amount_currency** | string | Yes | 3 | Payment currency Format: fiat currency code in ISO 4217 standard  Example: `USD` |
| **point** | object | No | — | A set of point parameters for payment creation. The parameters, that could possibly be passed inside of the `point` object are given below |
| point.callback_url | string | No | 1000 | URL for callback transmission to the merchant. See the Callbacks section for details. The parameter cannot be empty, must be valid and must not lead to an IP from the local network  ⚠️ We recommend correctly configuring `callback_url` to provide real-time transaction status updates |
| point.return_url | string | No | 1000 | URL to redirect the customer back to the merchant's site before the final transaction status is received |

### Request body parameters – fields

| Name | Type | Mandatory | Max. length | Description |
| --- | --- | --- | --- | --- |
| **fields** | object | No | — | Object with parameters for creating a transaction |
| fields.first_name | string | No | 50 | Customer's first name At least one word with two or more letters  Allowed: Latin letters (`A-Z` `a-z`), letters with diacritics (`Ñ` `ñ`), hyphens (`-`), apostrophes (`‘`) and spaces  Not allowed: numbers and other special symbols (`@` `#` `%` etc) |
| fields.last_name | string | No | 50 | Customer's last name At least one word with two or more letters  Allowed: Latin letters (`A-Z` `a-z`), letters with diacritics (`Ñ` `ñ`), hyphens (`-`), apostrophes (`‘`) and spaces  Not allowed: numbers and other special symbols (`@` `#` `%` etc) |
| fields.phone | string | No | 13 | Customers's phone number in international format The number starts with +593 and consists of 13 symbols  Format: `+593XXXXXXXXX`  Example: `+593991234567` |
| fields.email | string | No | 255 | Customer's email address Must contain the @ symbol and correct domain  Allowed: Latin letters in lower case (`a-z`), digits (`0-9`) and symbols (`@` `.` `_` `%` `+` `-`)  Format: `username@domain.extension`  Example: `example@mail.com` |
| fields.tax_id_type | string | No | 4 | Customer's document type:-   **CI** – national identity card -   **RUC** – tax identification number -   **PASS** – passport |
| fields.tax_id | string | No | 13 | Customer's document number:-   **CI** transmitted in the format: Number contains up to 10 digits  Allowed: digits (`0-9`)  Format: `XXXXXXXXXX`  Example: `1234567890` -   **RUC** transmitted in the format: Number consists of 13 digits  Allowed: digits (`0-9`)  Format: `XXXXXXXXXXXXX`  Example: `1234567890001` -   **PASS** transmitted in the format: Number contains from 5 to 13 characters  Allowed: digits (`0-9`) and Latin letters (`A-Z`)  Example: `FA123456` |

\* Without providing the parameter, the client will need to manually provide it on the payment page

**Optional parameters**

warning

Passing optional parameters can increase conversion rates and reduce transaction finalization time. Please contact the manager for details on the use of these parameters

| Name | Type | Mandatory | Max. length | Description |
| --- | --- | --- | --- | --- |
| fields.date_of_birth | string | No | 10 | Customer's date of birth in ISO 8601 standard Allowed: digits (`0-9`) and hyphens (`-`)  Format: `YYYY-MM-DD`  Example: `1992-03-19` |
| fields.address | string | No | 255 | Customer's full address  💡 If this parameter is not received from the merchant, we can compile it from the fields `city`, `street`, `building_number` and `zip_code` |
| fields.street | string | No | 100 | Customer's street name |
| fields.building_number | string | No | 10 | Customer's house number, related to the fields.street parameter |
| fields.district | string | No | 50 | Customer's district |
| fields.city | string | No | 50 | Customer's city |
| fields.state | string | No | 50 | Customer's state or province |
| fields.country | string | No | 2 | Customer's country Country code in ISO 3166-1 alpha-2 standard  Example: `EC` – Ecuador |
| fields.zip_code | string | No | 6 | Customer's postal code |

### Request body example

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
        "tax_id": "1234567890001",
        "date_of_birth": "1992-03-19",
        "address": "Quito, Selva Alegre, OE8-268, 170129",
        "street": "Selva Alegre",
        "building_number": "OE8-268",
        "district": "Rumipamba",
        "city": "Quito",
        "state": "Province of Pichincha",
        "country": "EC",
        "zip_code": "170129"
   }
}
```

### Response parameters

| Name | Type | Description |
| --- | --- | --- |
| **error** | object | Object with error data |
| error.code | integer | Error code. If no error occurs during processing, the error code is 0 |
| error.title | string | Error name |
| error.message | string | A detailed description of the error. Returned when an error is received with error.code other than 0 |
| **response** | object | Object with parameters of the performed request |
| response.account_id | integer | Merchant account ID in the payment gateway |
| response.amount | integer | Payment amount multiplied by 100 Format: positive integer without decimals  Examples:  `5000.00 USD` is transmitted as `500000` (5000.00 x 100 = 500000)  `1534.20 USD` is transmitted as `153420` (1534.20 x 100 = 153420) |
| response.amount_currency | string | Payment currency Format: fiat currency code in ISO 4217 standard  Example: `USD` |
| response.external_customer_id | string | Customer's ID in the merchant system |
| response.external_order_id | string | Order ID in the merchant system |
| response.external_transaction_id | string | Transaction ID in the merchant system |
| response.failure_reason_code | integer | Failure reason code. Returned in case of unsuccessful transaction status |
| response.failure_reason_message | string | Description of the failure reason code. Returned in case of unsuccessful transaction status |
| response.id | integer | Identifier of the created transaction in the payment gateway |
| response.is_test | boolean | Parameter indicating whether the transaction is a test one. Automatically affixed to all transactions created using a merchant's test account |
| response.point_id | integer | Payment acceptance point ID |
| response.result | object | The result of transaction creation. On success, contains the pay_url of the payment page |
| response.result.pay_url | string | Link to the payment page |
| response.service_id | integer | Payment gateway service ID |
| response.status | integer | Transaction status. The created transaction, if there is no error, will have a non-final status of 0 (NEW) or 10 (PENDING) |
| response.status_description | string | Description of the payment status (in case of unsuccessful status) |
| response.wallet_id | integer | Merchant wallet ID in the payment gateway |

## Redirection to the payment page

A transaction is considered successfully created once the unique payment page link (`pay_url`) is received. After that, the client can be redirected to this link in any convenient way.

## Waiting for the callback

After the customer navigates to the payment page, the merchant must wait for a callback from the betterbro payment gateway. It will be sent as soon as the transaction reaches a final status.

**Please note**: the payment will be credited with the actual amount paid by the customer, which may differ from the amount provided when creating the transaction. The final amount will be provided in the callback or in the response from /v2/transaction/find

## Transaction status

It is important to make decisions about the success or failure of a transaction based on the value of the `status` parameter in the callback or in the /v2/transaction/find response.

In some cases, an unsuccessful `2 (FAILED)`, `3 (CANCELLED)` or `5 (EXPIRED)` transaction status can be automatically changed to a successful `1 (SUCCESS)`. In case of such a change, the betterbro payment gateway will send a repeated callback to the merchant.

Automatic change of a successful status to any other is not possible
