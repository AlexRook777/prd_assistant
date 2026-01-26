I want to test HPP payment via the "wallet" method using this API: {PROVIDER_API_DOCUMENTATION_URL}.
I have provided all the necessary keys and credentials in configuration.

Phase 1: Create test page

Step 1: 
Create a test HTML page where I can enter all the required credentials, receive a payment link, open it in a new tab, and have the ability to click a button to check the payment status. After checking the status, the updated payment status should be displayed within the payment details on the page.

Step 2: Optionally allow me to specify a callback URL. There must be an option to view and copy all requests and responses (including headers). In the request log, besides the option to copy individual entries, add a button to copy the entire log (including URL, method, headers, body, and response).

Step 3: Design the page to be professional and user-friendly. However, the main priority is functional correctness and flexibility in configuring request parameters. Save all entered credentials in sessionStorage so I don't have to re-enter them every time the page reloads (but they should be cleared when the browser is closed).

Step 4: Webhook Verification
To test webhooks, use the following universal test URL: {TEST_POST_WEBHOOK_URL}, where: orderId is substituted dynamically and uniquely for each transaction.

To retrieve the list of webhooks received at this endpoint, use a GET request to {TEST_GET_WEBHOOK_URL} (this is protected by Basic Auth; I will enter the username and password in the form myself before creating a transaction).

After a transaction is created, attempt to fetch processed webhooks every 5 seconds and display the current list in the interface in chronological order. Additionally, add a button for a manual refresh. The response from this endpoint will be in the following format:

JSON

[
  {
    "_id": "694b97fc8faa2c4927f343f3",
    "callbackRawData": {
      "headers": {},
      "query": {},
      "body": {}
    },
    "timestamp": "2025-12-24T07:36:28.893Z",
    "timestampEpoch": 1766561788893,
    "callbackId": "orderId"
  }
]

Phase 2: Automation testing - proceed by agent
Testing Instructions:
1. Open the test page in a browser with CORS proxy.
2. Enter all the required credentials and click "Get Token".
3. Click "Create Transaction" to receive a payment link.
4. Open the payment link in a new tab and complete the payment.
5. Click "Check Payment Status" to verify the payment status.
6. View the request log to see all requests and responses.
7. Click "Copy Log" to copy the entire log (including URL, method, headers, body, and response).
8. Click "Refresh Webhooks" to fetch the list of webhooks received at the test endpoint.
9. View the webhooks list to see the processed webhooks in chronological order.
10. Click "Copy Webhooks" to copy the entire list of webhooks.
11. Write the test results in the file `1_research/3.local_test_page.md` as a new section "Test Results". 