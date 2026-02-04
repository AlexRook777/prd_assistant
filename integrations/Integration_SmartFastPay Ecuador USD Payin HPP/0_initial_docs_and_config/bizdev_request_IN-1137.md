# BizDev Integration Request: SmartFastPay Ecuador USD Payin HPP

- **Jira Link**: https://4billio.atlassian.net/browse/IN-1137
- **Issue Key**: IN-1137
- **Created At**: 2025-06-12T18:19:23.897+0300

## Description

По провайдеру буде опис від ВА. Спочатку робимо Bank Transfer і потім інші методи.

Стандратний HPP провайдера, де ми робимо запит, отримуємо пейурл. Дока не зовсім актуальна. Запит буде відрізнятись тим, що не треба передавати кастомер філдс в запиті на кріейт.

Інтеграцію робитимемо через їх [чекаут](https://docs.smartfastpay.com/thesmartway/checkout-experience/overview). Є можливість відобаржати сторінку на якій юзер буде вводити свої дані, якщо вони не передані в запиті. Якщо передані - відображаються передзаповненими.

Ecuador (all payment methods)

Limits per transaction:
- min 6 USD
- max 1 000 USD

Limits per user:
- max daily 1 200 USD
- max monthly 36 000 USD

Peru (all payment methods)

Limits per transaction:
- min 25 PEN (aprox 7 USD)
- max 3700 PEN (aprox 1 000 USD)

Limits per user:
- max daily 11 100 PEN (aprox 3 000 USD)
- max monthly 18 500 PEN (aprox 5 000 USD)

## Transaction Limits

| Country | Method | Min Transaction | Max Transaction | Daily User Limit | Monthly User Limit |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Ecuador | All | 6 USD | 1,000 USD | 1,200 USD | 36,000 USD |
| Peru | All | 25 PEN (~7 USD) | 3,700 PEN (~1,000 USD) | 11,100 PEN (~3,000 USD) | 18,500 PEN (~5,000 USD) |

## Integration Details - Q&A

| Questions | Answers |
| :--- | :--- |
| Посилання на первинний тред в slack | [Thread Link](https://4billio.slack.com/archives/C07K7DP3B38/p1748957297144249) |
| Це новий постачальник? | [YES] |
| Чи було дослідження  репутації ПУ? На чому заснована впевненість замовника в постачальнику? | Yes, they supply for other PSPs and merchants already known (example Mostbet PSE Colombia) |
| Юридичні питання (договори/додатки) підписано? | [YES] |
| Мерчанти яким це треба вже є (урли погоджені)? | [YES] |
| Умови та тарифи узгоджені? | [YES] |
| Які ліміти (мін та макс сума платежу), кількість транзакцій на день чи добу, обсяги по максимальній сумі на день (добу) чи місяць? | Description |
| Назва ТЕХНІЧНОГО чату з командою інтеграції (підтримки) з боку провайдера | To be created [Telegram] |
| Очікуваний бізнесом рівень конверсії | [70%+] |
| Перелік конкурентів у яких працює метод від цього постачальника | Monetix ([weltrade.com](https://www.weltrade.com/) Colombia) |
| Мерчанти які через конкурентів інтегрували цей метод | Mostbet (PSE Colombia) |
| Провайдер підтвердив 100%-ву відповідність документації до реального флоу фактично працюючих платіжних методів? | [YES] |
| Payment method (w2w, p2p, Acquiring, ApplePay, GooglePay, Bank transfer, Mobile Money, Wallet, Crypto, On-Ramp etc) | Ecuador Bank Transfer |
| Way (deposit/withdrawal) | [payIN] |
| Expected daily USD transaction volume, one month after launch | TBD |
| Для мерчанта це буде: HPP, HPP через iframe, H2H, H2H + наша форма, H2H + deeplink | HPP |
| Аргументація вибору h2h або hpp | HPP will show the provider's name for the merchants and risking loosing clients to them |
| New, backup, portfolio | Pagsmile [IN-680](https://4billio.atlassian.net/browse/IN-680) |
| Чи потрібно матчити інтеграцію (для каскаду чи бекапу) та з чим? | No |
| Перелік країн в яких запускаємо | Ecuador, Peru |
| Які мови потрібно підтримувати? | Spanish, English |
| Перелік валют у яких оплачуватиме кінцевий користувач | Ecuador (USD), Peru (PEN) |
| Тестові креди та доступи Є? Коли будуть? | Yes, already available at management@mailhub.services |
| Продові креди та доступи Є? Коли будуть? | Yes, already available at management@mailhub.services |
| Адмінка ПУ та доступи до неї Є? В кого? | Yes, already available at management@mailhub.services |
| Посилання на відео флоу | [Google Sheets Link](https://docs.google.com/spreadsheets/d/1HzZ0O61bYINtV-6XWMnwhJynBvLemGl_BLQ5Nr4wFKc/edit?gid=1715498002#gid=1715498002) |
| Посилання на актуальну документацію (чи postman колекцію) | [Docs Link](https://docs.smartfastpay.com/thesmartway/checkout-experience/overview) |
| Ключові мерчанти які будуть брати у нас це метод (для аналізу, що вони вже в нас беруть, які філдси можуть передавати) | Amount, name, tax_id_type, tax_id, email. |

## Comments

### Comment by Denys Badzo (14/Jul/25 6:08 AM)

Oleksandr Novak привіт. В тексті написано, що інтеграція буде HPP, а в таблиці - протилежне (H2H для мерчанта треба). Чому вірити?

Якщо звичайний редірект на HPP, то можна і за день зробити.

### Comment by o.hrachov (2026-01-30T11:39:16.371+0200)

BetterBro url: https://docs.betterbro.com/services/ecuador/bank_transfer/payin_hpp

## Key Links

- [SmartFastPay Checkout Docs](https://docs.smartfastpay.com/thesmartway/checkout-experience/overview)
- [BetterBro Integration Docs](https://docs.betterbro.com/services/ecuador/bank_transfer/payin_hpp)
- [Video Flow](https://docs.google.com/spreadsheets/d/1HzZ0O61bYINtV-6XWMnwhJynBvLemGl_BLQ5Nr4wFKc/edit?gid=1715498002#gid=1715498002)
- [Pagsmile Integration IN-680](https://4billio.atlassian.net/browse/IN-680)
- [Monetix Example](https://www.weltrade.com/)
