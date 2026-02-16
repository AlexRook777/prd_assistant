# BizDev Integration Request: Інтеграція SmartFastPay Ecuador USD Payin HPP

- **Jira Link**: https://4billio.atlassian.net/browse/IN-1137
- **Issue Key**: IN-1137
- **Created At**: 2025-06-12T18:19:23.897+0200

## Description

По провайдеру буде опис від ВА. Спочатку робимо Bank Transfer і потім інші методи.
Стандартний HPP провайдера, де ми робимо запит, отримуємо пейурл. Дока не зовсім актуальна. Запит буде відрізнятись тим, що не треба передавати кастомер філдс в запиті на кріейт.

Інтеграцію робитимемо через їх [чекаут](https://docs.smartfastpay.com/thesmartway/checkout-experience/overview). Є можливість відобаржати сторінку на якій юзер буде вводити свої дані, якщо вони не передані в запиті. Якщо передані - відображаються передзаповненими.

## Transaction Limits

### Ecuador (all payment methods)
- **Per transaction**:
    - Min: 6 USD
    - Max: 1,000 USD
- **Per user**:
    - Max Daily: 1,200 USD
    - Max Monthly: 36,000 USD

### Peru (all payment methods)
- **Per transaction**:
    - Min: 25 PEN (~7 USD)
    - Max: 3,700 PEN (~1,000 USD)
- **Per user**:
    - Max Daily: 11,100 PEN (~3,000 USD)
    - Max Monthly: 18,500 PEN (~5,000 USD)

## Integration Details - Q&A

| Questions | Answers |
|-----------|---------|
| Посилання на первинний тред в slack | https://4billio.slack.com/archives/C07K7DP3B38/p1748957297144249 |
| Це новий постачальник? | [YES] |
| Чи було дослідження репутації ПУ? На чому заснована впевненість замовника в постачальнику? | Yes, they supply for other PSPs and merchants already known (example Mostbet PSE Colombia) |
| Юридичні питання (договори/додатки) підписано? | [YES] |
| Мерчанти яким це треба вже є (урли погоджені)? | [YES] |
| Умови та тарифи узгоджені? | [YES] |
| Які ліміти (мін та макс сума платежу), кількість транзакцій на день чи добу, обсяги по максимальній сумі на день (добу) чи місяць? | Description |
| Назва ТЕХНІЧНОГО чату з командою інтеграції (підтримки) з боку провайдера | To be created [Telegram] |
| Очікуваний бізнесом рівень конверсії | [70%+] |
| Перелік конкурентів у яких працює метод від цього постачальника | Monetix (https://www.weltrade.com/ Colombia) |
| Мерчанти які через конкурентів інтегрували цей метод | Mostbet (PSE Colombia) |
| Провайдер підтвердив 100%-ву відповідність документації до реального флоу фактично працюючих платіжних методів? | [YES] |
| Payment method | Ecuador Bank Transfer |
| Way (deposit/withdrawal) | [payIN] |
| Expected daily USD transaction volume | TBD |
| Для мерчанта це буде: HPP, HPP через iframe, H2H, H2H + наша форма, H2H + deeplink | HPP |
| Аргументація вибору h2h або hpp | HPP will show the provider's name for the merchants and risking loosing clients to them |
| New, backup, portfolio | Pagsmile https://4billio.atlassian.net/browse/IN-680 |
| Чи потрібно матчити інтеграцію (для каскаду чи бекапу) та з чим? | No |
| Перелік країн в яких запускаємо | Ecuador, Peru |
| Які мови потрібно підтримувати? | Spanish, English |
| Перелік валют у яких оплачуватиме кінцевий користувач | Ecuador (USD), Peru (PEN) |
| Тестові креди та доступи Є? Коли будуть? | Yes, already available at management@mailhub.services |
| Продові креди та доступи Є? Коли будуть? | Yes, already available at management@mailhub.services |
| Адмінка ПУ та доступи до неї Є? В кого? | Yes, already available at management@mailhub.services |
| Посилання на відео флоу | [Video Flow Spreadsheet](https://docs.google.com/spreadsheets/d/1HzZ0O61bYINtV-6XWMnwhJynBvLemGl_BLQ5Nr4wFKc/edit?gid=1715498002#gid=1715498002) |
| Посилання на актуальну документацію (чи postman колекцію) | https://docs.smartfastpay.com/thesmartway/checkout-experience/overview |
| Ключові мерчанти які будуть брати у нас це метод | Amount, name, tax_id_type, tax_id, email. |

## Comments

### Comment by Denys Badzo (14/Jul/25 6:08 AM)
> Oleksandr Novak привіт. В тексті написано, що інтеграція буде HPP, а в табличці - протилежне (H2H для мерчанта треба). Чому вірити?
> Якщо звичайний редірект на HPP, то можна і за день зробити.

### Comment by o.hrachov (30/Jan/26 11:39 AM)
> BetterBro url: https://docs.betterbro.com/services/ecuador/bank_transfer/payin_hpp

## Key Links

- [Jira Issue IN-1137](https://4billio.atlassian.net/browse/IN-1137)
- [SmartFastPay Checkout Documentation](https://docs.smartfastpay.com/thesmartway/checkout-experience/overview)
- [BetterBro Ecuador Payin HPP Docs](https://docs.betterbro.com/services/ecuador/bank_transfer/payin_hpp)
- [Slack Thread](https://4billio.slack.com/archives/C07K7DP3B38/p1748957297144249)
- [Video Flow Spreadsheet](https://docs.google.com/spreadsheets/d/1HzZ0O61bYINtV-6XWMnwhJynBvLemGl_BLQ5Nr4wFKc/edit?gid=1715498002#gid=1715498002)
