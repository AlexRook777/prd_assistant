# BizDev Integration Request: Integration_Cobre Colombia COP Payout

- **Jira Link**: https://4billio.atlassian.net/browse/IN-1095
- **Issue Key**: IN-1095
- **Created At**: 2025-05-16

## Description

Payout по постачальнику Cobre, по якому вже робили задачу на [payin](https://4billio.atlassian.net/browse/IN-813)

В документації не описаний процес Payout окремо. Треба запустити Postman і на зустрічі з провайдером дізнатись як відбувається процес. Скоріш за все це той же метод money movements і аналогічний флоу як по пейіну. Треба дослідити через ВА.

Після релізу треба буде провести приймальне тестування з постачальником.

## Transaction Limits

No specific limits mentioned in the description.

## Integration Details - Q&A

| Question | Answer |
| :--- | :--- |
| 1. Економічне обгрунтування задачі. І хто це приніс і скільки часу в нас на реалізацію. | Задачу будемо робити з описом ВА. Далі рухати в хаєст |
| 2. Який платіжний метод (еквайринг / р2р / а2с / АП, ДП / і т.д.)? | PSE Payout |
| 3. Чи є замовник вже на цю інтеграцію? | так |
| 4. Описаний чи записаний to be? (простими словами як ви хочете що б ця задача працювала) | стандартний пейаут без сторінки проміжної. |
| 5. Яке це рішення - Нове, Єдине, Бєкап | Нове |
| 6. Чи потрібно робити інтеграцію в каскад з іншими? | Ні.Але треба буде перелянути рішення від Bitso, чи схожий флоу |
| 7. Чи було дослідження ринку і чи ця інтеграція має загальний флоу для їй подібних? | загальний флоу |
| 8. Яку платіжну сторінку використовуємо (нашу/провайдера)? | без сторінки |
| 9. Документація (postman колекція) | [https://developers.cobre.co/](https://developers.cobre.co/) |
| 10. Чи є чат з провайдером і чи можливо туди додати БА | чат в слак |
| 11. У якій валюті шлюз відправлятиме провайдеру (перелік валют, які приймає провайдер) | COP |
| 12. У якій валюті оплачуватиме кінцевий користувач? | COP |
| 13. Чи є тестові креди? | так, у операціоністів та в PM Віталій |
| 14. Чи є тестові карти (параметри) за різними сценаріями? | ні |

## Other

- **Context**: This is a Payout integration for Cobre in Colombia.
- **Previous Work**: Payin was implemented in IN-813.
- **Provider Contact**: Slack channel exists.
- **Testing**: Ops team and PM Vitaliy have credentials. No test cards.

## Comments

### Comment by Maxim Lukianenko (12/Jun/25 12:00 PM)

@Yurii Bilyk Добрий день!
@Oleksandr Novak @Andrii Diachenko @Svitlana Bilous FYI

Прикріпив опис до задачі, прохання глянути і дати зворотній зв'язок.
Мапінг помилок та АС на доописі, протягом 2 годин буде додано у файл.

Дякую!

### Comment by o.hrachov (Today 1:57 PM)

https://docs.betterbro.com/services/latam/colombia/pse/payout

## Key Links

- [https://4billio.atlassian.net/browse/IN-813](https://4billio.atlassian.net/browse/IN-813)
- [https://developers.cobre.co/](https://developers.cobre.co/)
- [https://docs.betterbro.com/services/latam/colombia/pse/payout](https://docs.betterbro.com/services/latam/colombia/pse/payout)

## Context from Related Integration (IN-813 - Payin)

**This section contains information extracted from the related Payin task (IN-813) to provide context and potential technical details. verified by the developer.**

- **Endpoints**:
    - **Create Money Movement**: `POST https://api.cobre.co/v1/money_movements`
    - **Create Counterparty**: `POST https://developers.cobre.co/docs/Platformv3/t41x2dpusakcl-create-new-counterparty` (Likely needed if counterparty doesn't exist)
- **Flow Insights**:
    - IN-813 describes a flow where a "Parent" transaction is created, followed by a "Child" transaction.
    - If a counterparty ID is not stored, the connector creates one via the API.
    - The `money_movements` endpoint returns a `pay_url` (for payins), but for payouts, it might return a status or different data.
- **Callback Example (Payin)**:
    ```json
    {
      "process": "Cobre Payin HPP process callback.",
      "callback_json": {
        "id": "ev_T5feVv7E60eKs5X4Joli",
        "event_key": "money_movements.status.completed",
        "created_at": "2025-04-09T09:04:01Z",
        "content": {
          "id": "mm_NH3ttjs9MSAsHQ",
          "status": {
            "state": "completed",
            "code": "",
            "description": ""
          },
          "amount": 199,
          "currency": "cop"
        }
      }
    }
    ```
- **Credentials**: Confirmed available with Ops team and PM Vitaliy.
- **Slack Channel**: A dedicated channel exists (link in IN-813 comments).
