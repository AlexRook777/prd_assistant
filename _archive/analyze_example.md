SmartFastPay API Testing Report - Chile Bank Transfer





SmartFastPay API Testing Report
Chile / Bank Transfer (Payin)
Дата тестування: 2025-12-31  
Середовище: Sandbox (https://sandbox.smartfastpay.com)  
Документація: https://docs.smartfastpay.com/methods-and-markets/payin/latam/chile/bank-transfer

1. Автентифікація
Запит


curl -s -X POST https://sandbox.smartfastpay.com/oauth2/token \
  -H "Content-Type: application/json" \
  -u "CLIENT_ID:CLIENT_SECRET" \
  -d "{}"
Відповідь


{
  "requestId": "50a4fec528f790ba2ac07745edbc66f9/14917398851859663102;o=1",
  "data": {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "Bearer",
    "expires_in": 3600
  }
}
⚠️ Зауваження
Документація не вказує, що потрібно передавати тіло запиту {}. Без нього API повертає HTTP 411 (Length Required).

2. Створення транзакції (POST /v2/payin)
Успішний запит


curl -s -X POST https://sandbox.smartfastpay.com/v2/payin \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{
    "customer": {
        "id": "cust-chile-001",
        "name": "Juan Pablo Rodriguez",
        "email": "juan.rodriguez@test.com",
        "document": {
            "number": "18667538",
            "type": "CI"
        },
        "phone": "+56956249181"
    },
    "transaction": {
        "id": "test-chl-bt-1767180330",
        "currency": "CLP",
        "amount": 50000
    },
    "country": "CHL",
    "payment_method": "bank_transfer",
    "notification_url": "https://example.com/webhook/test-chl-bt-1767180330"
}'
Відповідь


{
  "requestId": "34381583f17fa64f9d1870c2ed5345e5/11010823351262177036;o=1",
  "data": {
    "id": "07e24bca-eeb6-468d-87db-456c75672cf2",
    "status": "pending",
    "expires_in": 1767182131,
    "payment": {
      "method": "bank_transfer",
      "url": "https://paykugateway-frontend.payku.cl/cobro/..."
    },
    "values": {
      "source_total": "50000.00000000",
      "source_currency": "CLP",
      "exchanged_total": "50000.00",
      "exchanged_currency": "CLP",
      "exchange": "1.00",
      "fee": "500.00000000"
    }
  }
}
🔴 Невідповідність #1: Типи даних у values
Поле

Документація

Фактично

source_total

27525.47 (number)

"50000.00000000" (string)

exchanged_total

27525.47 (number)

"50000.00" (string)

exchange

1.00 (number)

"1.00" (string)

fee

0 (number)

"500.00000000" (string)

3. Отримання статусу транзакції
3.1 GET /transaction/{id}


curl -s -X GET "https://sandbox.smartfastpay.com/transaction/07e24bca-eeb6-468d-87db-456c75672cf2" \
  -H "Authorization: Bearer <token>"
Відповідь:



{
  "data": {
    "id": "07e24bca-eeb6-468d-87db-456c75672cf2",
    "customer_id": "cust-chile-001",
    "transaction_id": "test-chl-bt-1767180330",
    "amount": "50000.00000000",
    "currency": "CLP",
    "status": "pending",
    "method": "bank_transfer",
    "created_at": "2025-12-31T11:25:31.000000Z",
    "updated_at": "2025-12-31T11:25:32.000000Z",
    "type": "payment",
    "payment_status": "pending"
  }
}
3.2 GET /payment/{id}
Відповідь:



{
  "data": {
    "id": "07e24bca-eeb6-468d-87db-456c75672cf2",
    "customer_id": "cust-chile-001",
    "transaction_id": "test-chl-bt-1767180330",
    "amount": "50000.00000000",
    "currency": "CLP",
    "status": "pending",
    "method": "bank_transfer",
    "created_at": "2025-12-31 08:25:31",
    "updated_at": "2025-12-31 08:25:32"
  }
}
🔴 Невідповідність #2: Формат дати
Endpoint

Формат created_at

GET /transaction/{id}

"2025-12-31T11:25:31.000000Z" (ISO 8601)

GET /payment/{id}

"2025-12-31 08:25:31" (нестандартний, інший час!)

3.3 GET /payments (list)
Відповідь:



{
  "data": [{
    "id": "07e24bca-eeb6-468d-87db-456c75672cf2",
    "created_at": null,
    "updated_at": null
  }]
}
🔴 Невідповідність #3: created_at та updated_at = null
4. Створені тестові транзакції
Order ID

Internal ID

Сума

Результат на платіжній сторінці

Статус в API

test-chl-bt-1767180330

07e24bca-eeb6-468d-87db-456c75672cf2

50,000 CLP

✅ SUCCESS

❌ pending

test-no-phone-001

3253ba06-6fdd-4750-91b9-273a09b071b7

5,000 CLP

✅ SUCCESS

❌ pending

test-str-amount

501d598d-e4b2-41d1-a60d-fdbcc9eec82f

5,000 CLP

❌ FAILED

❌ pending

🔴 КРИТИЧНА ПРОБЛЕМА #1: Статус не синхронізується
Після фіналізації транзакцій на платіжній сторінці провайдера (Payku), статус в API SmartFastPay залишається pending. Транзакції фіналізовані о ~13:00 UTC, перевірено через 30+ хвилин — статус не змінився.

🔴 КРИТИЧНА ПРОБЛЕМА #2: Webhooks не відправляються
Жодна з фіналізованих транзакцій не відправила webhook на notification_url.

5. Валідаційні тести
✅ Працює коректно
Тест

Запит

Відповідь

Missing customer.name

без поля name

"The customer.name field is required."

Invalid document type

"type": "INVALID_TYPE"

"Document type INVALID_TYPE not found"

Negative amount

"amount": -1000

"The transaction.amount must be greater than 0."

Zero amount

"amount": 0

"The transaction.amount must be greater than 0."

Wrong currency

"currency": "USD" для CHL

"It is not possible to have transactions in this currency USD for the informed country CHL"

Duplicate transaction ID

Повторний transaction.id

"The transaction.id has already been taken."

Missing notification_url

Без поля

"The notification url field is required."

Long name (>150)

250+ символів

"The customer.name must not be greater than 150 characters."

Invalid email

"email": "not-an-email"

"The customer.email must be a valid email address."

🔴 Проблеми валідації
Некоректний country code → 500
Запит: "country": "CHILE" (замість "CHL")

Відповідь:



{
  "status": "INTERNAL_SERVER_ERROR",
  "payload": { ... }
}
Очікувано: HTTP 400 з повідомленням про невалідний код країни  
Фактично: HTTP 500 INTERNAL_SERVER_ERROR

Без customer.email → 500
Документація вказує customer.email як optional (required: no).

Відповідь:



{
  "status": "INTERNAL_SERVER_ERROR",
  "payload": { ... }
}
Очікувано: Успішне створення транзакції (поле optional)  
Фактично: HTTP 500 INTERNAL_SERVER_ERROR

transaction.amount з десятковими
Документація вказує тип decimal(10,2).

Запит: "amount": 1000.50

Відповідь:



{
  "moreInformation": [{
    "code": "INVALID_REQUEST",
    "detail": "The transaction.amount must be an integer."
  }]
}
Очікувано: Приймає decimal(10,2)  
Фактично: Вимагає integer для CLP (логічно, але не задокументовано)

6. Зведена таблиця невідповідностей
🔴 Критичні (блокують інтеграцію)
#

Проблема

Деталі

1

Webhooks не відправляються

Після фіналізації транзакцій (success/fail) жоден webhook не надійшов на notification_url

2

Статус не оновлюється

GET endpoints повертають status: "pending" навіть після успішної/неуспішної оплати

3

customer.email required

Документація: optional. Фактично: без email → 500 Internal Server Error

🟠 Середні (невідповідність документації)
#

Проблема

Документація

Фактично

4

Invalid country → 500

Має бути 400

500 Internal Server Error

5

values.* типи

Numbers

Strings

6

transaction.amount тип

decimal(10,2)

integer для CLP

7

Формат created_at

ISO 8601

Різний на різних endpoints

8

GET /payments created_at

Має бути заповнений

null

🟡 Низькі (зауваження)
#

Проблема

9

customer.phone є в прикладі, але відсутній в таблиці параметрів

10

OAuth потребує {} в body (не документовано)

11

GET /transaction приймає тільки internal UUID, не merchant transaction_id

12

transaction.amount приймає string (недокументовано)

13

Помилка "notification url" (пробіл) vs параметр notification_url (underscore)

7. Питання до постачальника
Чому webhooks не відправляються в sandbox? Чи є спосіб протестувати отримання callbacks?

Чому статус транзакцій не оновлюється після фіналізації? Яка очікувана затримка синхронізації?

customer.email обов'язковий для Chile/bank_transfer? Документація вказує optional.

Який правильний тип для transaction.amount? Документація вказує decimal(10,2), але API вимагає integer для CLP.

Чому values повертаються як strings замість numbers? Це очікувана поведінка чи баг?

Звіт підготовлено на основі тестування API 2025-12-31