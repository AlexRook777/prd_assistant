# BizDev Integration Request: Integration_Bankizi Brazil BRL Payin H2H

- **Jira Link**: https://4billio.atlassian.net/browse/IN-1224
- **Issue Key**: IN-1224
- **Created At**: 2025-09-10T21:08:14.211+0300

## Description

Стандратний новий пікс в каскад до провайдера Infinia. ЧИ можемо взяти без опису ВА?

### PIX PayIn Flow (Bankizi API)

#### 1. Авторизація
`Authorization: Bearer {{AUTH_TOKEN}}`
Використовується у всіх запитах у заголовку `Authorization`.

#### 2. Створення транзакції (Cash In)
**Endpoint:** `POST /charges/pix`

**Body (JSON):**
```json
{
  "amount": 1000,                 
  "expiration": 3600,             
  "payerInfo": {
    "document": "12345678901", // Важливо. Треба зробити можливість для операціоністів не передавати це поле на провайдера. Якщо передаємо це поле - воно має матчитись з фактичними даними при оплаті. Але транзакція буде створюватись якщо не передавати цей параметр при запиті
    "name": "João da Silva"
  },
  "txId": "unique_tx_001"
}
```

**Response:**
```json
{
  "qrCode": "00020101021226...",
  "amount": 1000,
  "transactionId": "3f7a7e50-...",
  "txId": "unique_tx_001"
}
```

#### 3. Статуси (Cash In)
- `GENERATED` — транзакція створена.
- `PAID` — оплата завершена.
- `REQUESTED_REFUND` — запит на повернення.
- `REFUNDED` / `PARTIALLY_REFUNDED` — повернено повністю / частково.

#### 4. Колбек (Webhook)
**Подія:** `PIX_IN`

**Payload:**
```json
{
  "event": "PIX_IN",
  "data": {
    "txId": "unique_tx_001",
    "transactionId": "3f7a7e50-...",
    "endToEndId": "E123456789...",
    "status": "PAID",
    "amount": 1000,
    "payerInfo": {
      "name": "João da Silva",
      "document": "12345678901"
    }
  }
}
```

#### 5. Check Status
**Endpoint:** `GET /transactions/{id}`

**Response:**
```json
{
  "endToEndId": "E123456789...",
  "txId": "unique_tx_001",
  "transactionId": "3f7a7e50-...",
  "amount": 1000,
  "status": "PAID"
}
```

#### 6. Balance
**Endpoint:** `GET /balance`

**Response:**
```json
{
  "available": 150000,
  "currency": "BRL"
}
```

Також з важливого. Мапінг помилок поки що відсутній. Провайдер намагається зібрати і надати перелік своїх помилок.

## Transaction Limits

- **Min Amount**: -
- **Max Amount**: -
- **Daily Count/Volume**: -
- **Monthly Volume**: -

## Integration Details - Q&A

| Questions | Answers |
| :--- | :--- |
| Посилання на первинний тред в slack | - |
| Це новий постачальник? | так |
| Мерчанти яким це треба вже є (урли погоджені)? | урли погоджені |
| Умови та тарифи узгоджені? | так |
| Які ліміти (мін та макс сума платежу), кількість транзакцій на день чи добу, обсяги по максимальній сумі на день (добу) чи місяць? | - |
| Назва ТЕХНІЧНОГО чату з командою інтеграції (підтримки) з боку провайдера | BetterBro & BankIzi [TECH] |
| Очікуваний бізнесом рівень конверсії | - |
| Перелік конкурентів у яких працює метод від цього постачальника | - |
| Мерчанти які через конкурентів інтегрували цей метод | - |
| Провайдер підтвердив 100%-ву відповідність документації до реального флоу фактично працюючих платіжних методів? | + |
| Payment method (w2w, p2p, Acquiring, ApplePay, GooglePay, Bank transfer, Mobile Money, Wallet, Crypto, On-Ramp etc) | PIX |
| Way (deposit/withdrawal) | deposit |
| Expected daily USD transaction volume, one month after launch |   |
| Для мерчанта це буде: HPP, HPP через iframe, H2H, H2H + наша форма, H2H + deeplink | наша форма + h2h |
| Аргументація вибору h2h або hpp | треба в каскад до поточної інфінії |
| New, backup, portfolio | каскад з Інфініа і Віртуалпей |
| Чи потрібно матчити інтеграцію (для каскаду чи бекапу) та з чим? | Інфініа і Віртуалпей |
| Перелік країн в яких запускаємо | Бразилія |
| Які мови потрібно підтримувати? | PT/BR |
| Перелік валют у яких оплачуватиме кінцевий користувач | BRL |
| Тестові креди та доступи Є? Коли будуть? | + |
| Продові креди та доступи Є? Коли будуть? | + |
| Адмінка ПУ та доступи до неї Є? В кого? | + |
| Посилання на відео флоу |   |
| Посилання на актуальну документацію (чи postman колекцію) | [https://documenter.getpostman.com/view/41941457/2sB2cX7LMF#intro](https://documenter.getpostman.com/view/41941457/2sB2cX7LMF#intro) |
| Ключові мерчанти які будуть брати у нас це метод (для аналізу, що вони вже в нас беруть, які філдси можуть передавати) |   |

## Other

- Base URL (Stage): `https://s1krem3dgj.execute-api.us-east-1.amazonaws.com/api`

## Comments

### Comment by Maksym Vovk (15/Sep/25 2:35 PM)
команди: con

Dev 12h qa 24h

### Comment by o.hrachov (Today 1:21 PM)
https://docs.betterbro.com/services/latam/brazil/pix/payin_h2h

## Key Links

- [Documentation (Postman)](https://documenter.getpostman.com/view/41941457/2sB2cX7LMF#intro)
- [Staging Base URL](https://s1krem3dgj.execute-api.us-east-1.amazonaws.com/api)
- [BetterBro Service Rules](https://docs.betterbro.com/services/latam/brazil/pix/payin_h2h)
