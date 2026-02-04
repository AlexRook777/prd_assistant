# Bank Transfer Payin HPP

**Bank Transfer** are a common payment method in Ecuador, with over 8 million users. Transfers are made in US dollars, and the process requires users to copy the recipient's account number and paste it into their banking app. If the entered amount differs from the expected transaction, the transfer still completes, and the merchant receives the actual amount sent.

[ ![Logo](/img/method_logos/ecuador/bank_transfer/darkmode.png) ](https://docs.betterbro.com/downloads/method_logos/ecuador/bank_transfer.zip)

![](/icons/notification/info.svg)
You can find more information about this method and the video flow on our [Knowledge Hub](https://hub4merchant.notion.site/ecuador#1dfee5da506f809b8b0af07a3cbc6a0f) portal

## Payment flow[​](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#payment-flow)

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

## Create a transaction[​](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#create-a-transaction)

To create a transaction, use the [/v2/transaction/create](https://docs.betterbro.com/api/v2/transaction/create) endpoint.

Data exchange with the payment gateway API is performed exclusively in **JSON** format via the **POST** method. Each request must include the **Content-Type: application/json** header; otherwise, it will be considered invalid, even if the body contains valid JSON.

### Authentication[​](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#authentication)

To successfully [authenticate](https://docs.betterbro.com/request_format#authentication), all requests must contain valid **JSON** and include the following headers:

| Header | Description |
| --- | --- |
| X-Timestamp | Current timestamp generated directly before sending the request Format: Unix timestamp with **one-second** precision Example: `1766129276` During request processing, it is verified that the current time does not exceed the **X-Timestamp** value by more than **60 seconds**. If this condition is not met, the request will be rejected with [10 BAD_REQUEST](https://docs.betterbro.com/reference/api_error_codes) error and the message: **The request is out of date** |
| X-Point-ID | Identifier of the point from which the request originates (`point_id`). It is used to determine the point's API token, which is required to verify the **X-Signature** Example: `556` |
| X-Signature | The cryptographic signature is [calculated](https://docs.betterbro.com/request_format#calculating-x-signature) using the **HMAC SHA256** hashing algorithm. For validation, the payment gateway recalculates the signature using the request body and the point's API token. If the values do not match, the request is rejected with error code [11 INVALID_AUTH](https://docs.betterbro.com/reference/api_error_codes) Example: `d96180fe66442b2d0bf458e8a33e6e6d7867546ce136432c79afbf9e0297ee2a` |

### Request body parameters[​](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#request-body-parameters)

| Name | Type | Mandatory | Max. length | Description |
| --- | --- | --- | --- | --- |
| **locale** | string | Yes | 2 | Language of the payment page Format: language code in the [ISO 639-1](https://docs.betterbro.com/reference/language_codes) standard Examples: `es` – Spanish, `en` – English |
| **external_customer_id** | string | Yes | 45 | Customer's ID in the merchant's system. Used for improvement of the transaction's search during incidents analysis, as well as for the operation of the anti-fraud system. If such parameter is absent in the system, it is necessary to send an alternative value for payer's identification, for example: mobile phone number or email |
| **customer_ip_address** | string | Yes | 39 | Customer's IP address. Both IPv4 and IPv6 addresses are allowed. It is important to send the customer's real IP to avoid false positives in the anti-fraud system |
| **external_transaction_id** | string | Yes | 128 | Transaction ID in the merchant system. Must be unique for each transaction. If a transaction already exists with the same `point_id` and `external_transaction_id`, payment creation will be rejected with an error [203](https://docs.betterbro.com/reference/api_error_codes) |
| **external_order_id** | string | No | 48 | Order ID in the merchant system. It is allowed to create multiple transactions with the same `external_order_id` |
| **account_id** | integer | Yes | — | Merchant account ID in the payment gateway. Provided by the **betterbro** manager |
| **wallet_id** | integer | Yes | — | Merchant wallet ID in the payment gateway. Provided by the **betterbro** manager |
| **service_id** | integer | Yes | — | Payment gateway service ID. Provided by the **betterbro** manager |
| **description** | string | No | 100 | Description of payment purpose |
| **amount** | integer | Yes | — | Payment amount multiplied by 100 Format: positive integer without decimals Examples: `5000.00 USD` is transmitted as `500000` (5000.00 x 100 = 500000) `1534.20 USD` is transmitted as `153420` (1534.20 x 100 = 153420) |
| **amount_currency** | string | Yes | 3 | Payment currency Format: fiat currency code in [ISO 4217](https://docs.betterbro.com/reference/currency_codes) standard Example: `USD` |
| **point** | object | No | — | A set of point parameters for payment creation. The parameters, that could possibly be passed inside of the `point` object are given below |
| point.**callback_url** | string | No | 1000 | URL for callback transmission to the merchant. See the [Callbacks](https://docs.betterbro.com/callbacks) section for details. The parameter cannot be empty, must be valid and must not lead to an IP from the local network ⚠️ We recommend correctly configuring `callback_url` to provide real-time transaction status updates |
| point.**return_url** | string | No | 1000 | URL to redirect the customer back to the merchant's site before the final transaction status is received |

### Request body parameters – fields[​](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#request-body-parameters--fields)

| Name | Type | Mandatory | Max. length | Description |
| --- | --- | --- | --- | --- |
| **fields** | object | No[\*] | — | Object with parameters for creating a transaction |
| fields.**first_name** | string | No[\*] | 50 | Customer's first name At least one word with two or more letters Allowed: Latin letters (`A-Z` `a-z`), letters with diacritics (`Ñ` `ñ`), hyphens (`-`), apostrophes (`‘`) and spaces Not allowed: numbers and other special symbols (`@` `#` `%` etc) |
| fields.**last_name** | string | No[\*] | 50 | Customer's last name At least one word with two or more letters Allowed: Latin letters (`A-Z` `a-z`), letters with diacritics (`Ñ` `ñ`), hyphens (`-`), apostrophes (`‘`) and spaces Not allowed: numbers and other special symbols (`@` `#` `%` etc) |
| fields.**phone** | string | No[\*] | 13 | Customers's phone number in international format The number starts with +593 and consists of 13 symbols Format: `+593XXXXXXXXX` Example: `+593991234567` |
| fields.**email** | string | No[\*] | 255 | Customer's email address Must contain the @ symbol and correct domain Allowed: Latin letters in lower case (`a-z`), digits (`0-9`) and symbols (`@` `.` `_` `%` `+` `-`) Format: `username@domain.extension` Example: `example@mail.com` |
| fields.**tax_id_type** | string | No[\*] | 4 | Customer's document type:- **CI** – national identity card - **RUC** – tax identification number - **PASS** – passport |
| fields.**tax_id** | string | No[\*] | 13 | Customer's document number:- **CI** transmitted in the format: Number contains up to 10 digits Allowed: digits (`0-9`) Format: `XXXXXXXXXX` Example: `1234567890` - **RUC** transmitted in the format: Number consists of 13 digits Allowed: digits (`0-9`) Format: `XXXXXXXXXXXXX` Example: `1234567890001` - **PASS** transmitted in the format: Number contains from 5 to 13 characters Allowed: digits (`0-9`) and Latin letters (`A-Z`) Example: `FA123456` |

_\* Without providing the parameter, the client will need to manually provide it on the payment page_

**Optional parameters**

warning
Passing optional parameters can increase conversion rates and reduce transaction finalization time. Please contact the manager for details on the use of these parameters

| Name | Type | Mandatory | Max. length | Description |
| --- | --- | --- | --- | --- |
| fields.**date_of_birth** | string | No | 10 | Customer's date of birth in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) standard Allowed: digits (`0-9`) and hyphens (`-`) Format: `YYYY-MM-DD` Example: `1992-03-19` |
| fields.**address** | string | No | 255 | Customer's full address 💡 If this parameter is not received from the merchant, we can compile it from the fields `city`, `street`, `building_number` and `zip_code` |
| fields.**street** | string | No | 100 | Customer's street name |
| fields.**building_number** | string | No | 10 | Customer's house number, related to the fields.**street** parameter |
| fields.**district** | string | No | 50 | Customer's district |
| fields.**city** | string | No | 50 | Customer's city |
| fields.**state** | string | No | 50 | Customer's state or province |
| fields.**country** | string | No | 2 | Customer's country Country code in [ISO 3166-1 alpha-2](https://docs.betterbro.com/reference/country_codes) standard Example: `EC` – Ecuador |
| fields.**zip_code** | string | No | 6 | Customer's postal code |

### Request body example[​](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#request-body-example)

Below is an example of the request body (payload), you can get a full example of the request in the [Request format](https://docs.betterbro.com/request_format#request-example) section.

Request: /v2/transaction/create

```json
{    "locale": "es",    "external_customer_id": "123",    "customer_ip_address": "166.139.8.122",    "external_transaction_id": "1234567890",    "account_id": 123,    "wallet_id": 123,    "service_id": 123,    "description": "Test payment",    "amount": 500000,    "amount_currency": "USD",    "point": {        "callback_url": "https://your.server.callback.url",        "return_url": "https://your.server.return.url"    },    "fields": {        "first_name": "John",        "last_name": "Doe",        "phone": "+593991234567",        "email": "example@mail.com",        "tax_id_type": "RUC",        "tax_id": "1234567890001",        // Below are optional parameters        "date_of_birth": "1992-03-19",        "address": "Quito, Selva Alegre, OE8-268, 170129",        "street": "Selva Alegre",        "building_number": "OE8-268",        "district": "Rumipamba",        "city": "Quito",        "state": "Province of Pichincha",        "country": "EC",        "zip_code": "170129"   }}
```

### Response parameters[​](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#response-parameters)

All API responses, regardless of request outcome, contain an `error` object with error information. If a request or server error occurs, the `error` object will contain detailed information about the issue. If no error occurs during processing, the error code will be 0 and response will contain a `response` object with the parameters of the created transaction.

| Name | Type | Description |
| --- | --- | --- |
| **error** | object | Object with error data |
| error.**code** | integer | [Error code](https://docs.betterbro.com/reference/api_error_codes). If no error occurs during processing, the error code is 0 |
| error.**title** | string | Error name |
| error.**message** | string | A detailed description of the error. Returned when an error is received with `error.code` other than 0 |
| **response** | object | Object with parameters of the performed request |
| response.**account_id** | integer | Merchant account ID in the payment gateway |
| response.**amount** | integer | Payment amount multiplied by 100 Format: positive integer without decimals Examples: `5000.00 USD` is transmitted as `500000` (5000.00 x 100 = 500000) `1534.20 USD` is transmitted as `153420` (1534.20 x 100 = 153420) |
| response.**amount_currency** | string | Payment currency Format: fiat currency code in [ISO 4217](https://docs.betterbro.com/reference/currency_codes) standard Example: `USD` |
| response.**external_customer_id** | string | Customer's ID in the merchant system |
| response.**external_order_id** | string | Order ID in the merchant system |
| response.**external_transaction_id** | string | Transaction ID in the merchant system |
| response.**failure_reason_code** | integer | Failure reason code (see [Failure reason codes](https://docs.betterbro.com/reference/failure_reason_codes)). Returned in case of unsuccessful transaction status |
| response.**failure_reason_message** | string | Description of the failure reason code. Returned in case of unsuccessful transaction status |
| response.**id** | integer | Identifier of the created transaction in the payment gateway |
| response.**is_test** | boolean | Parameter indicating whether the transaction is a test one. Automatically affixed to all transactions created using a merchant's test account |
| response.**point_id** | integer | Payment acceptance point ID |
| response.**result** | object | The result of transaction creation. On success, contains the `pay_url` of the payment page |
| response.result.**pay_url** | string | Link to the payment page |
| response.**service_id** | integer | Payment gateway service ID |
| response.**status** | integer | Transaction status (see [Transaction statuses](https://docs.betterbro.com/reference/transaction_statuses)) The created transaction, if there is no error, will have a non-final status of `0 (NEW)` or `10 (PENDING)` |
| response.**status_description** | string | Description of the payment status (in case of unsuccessful status) |
| response.**wallet_id** | integer | Merchant wallet ID in the payment gateway |

### Response examples[​](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#response-examples)

Response: /v2/transaction/create (Successful)
```json
{    "error": {        "code": 0,        "title": "Success"    },    "response": {        "account_id": 123,        "amount": 500000,        "amount_currency": "USD",        "external_customer_id": "123",        "external_order_id": "100",        "external_transaction_id": "1234567890",        "id": 1234567890,        "is_test": false,        "point_id": 111,        "result": {            "pay_url": "https://payment.page.url"        },        "service_id": 123,        "status": 10,        "status_description": "",        "wallet_id": 123    }}
```

## Redirection to the payment page[​](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#redirection-to-the-payment-page)

A transaction is considered successfully created once the unique payment page link (`pay_url`) is received. After that, the client can be redirected to this link in any convenient way. Detailed information on usage and configuration is available in the [Payment page](https://docs.betterbro.com/payment_page) section.

## Waiting for the callback[​](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#waiting-for-the-callback)

After the customer navigates to the payment page, the merchant must wait for a [callback](https://docs.betterbro.com/callbacks) from the **betterbro** payment gateway. It will be sent as soon as the transaction reaches a final status.

![](/icons/notification/danger.svg)
**Please note**: the payment will be credited with the actual amount paid by the customer, which may differ from the amount provided when creating the transaction. The final amount will be provided in the [callback](https://docs.betterbro.com/callbacks) or in the response from [/v2/transaction/find](https://docs.betterbro.com/api/v2/transaction/find)

## Transaction status[​](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#transaction-status)

It is important to make decisions about the success or failure of a transaction based on the value of the `status` parameter in the [callback](https://docs.betterbro.com/callbacks) or in the [/v2/transaction/find](https://docs.betterbro.com/api/v2/transaction/find) response.

In some cases, an unsuccessful `2 (FAILED)`, `3 (CANCELLED)` or `5 (EXPIRED)` transaction status can be automatically changed to a successful `1 (SUCCESS)`.

![](/icons/notification/warning.svg)
Automatic change of a successful status to any other is **not possible**

## Additional transaction data[​](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#additional-transaction-data)

When a transaction reaches a successful [status](https://docs.betterbro.com/reference/transaction_statuses), the [callback](https://docs.betterbro.com/callbacks) or the response from the [/v2/transaction/find](https://docs.betterbro.com/api/v2/transaction/find) may include additional transaction details (for example, customer, payer, or payment data).

## See also[​](https://docs.betterbro.com/services/latam/ecuador/bank_transfer/payin_hpp#see-also)

- [Telegram bot](https://docs.betterbro.com/telegrambot)
- [Merchant dashboard](https://docs.betterbro.com/cabinet/general/overview)
- [References](https://docs.betterbro.com/category/references)
- [API endpoints](https://docs.betterbro.com/api/v2/list)
- [Callbacks](https://docs.betterbro.com/callbacks)
- [Reports](https://docs.betterbro.com/reports)
