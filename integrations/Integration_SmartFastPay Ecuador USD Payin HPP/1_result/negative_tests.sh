#!/bin/bash
TOKEN="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJodHRwczovL3NhbmRib3guc21hcnRmYXN0cGF5LmNvbS9vYXV0aDIvdG9rZW4iLCJpYXQiOjE3NzAwMjkwNjcsImV4cCI6MTc3MDAzMjY2NywibmJmIjoxNzcwMDI5MDY3LCJqdGkiOiJCc0c1anFBbng0Wk9pR3pIIiwic3ViIjoiMjgiLCJwcnYiOiIyNGE3ODQ1MTlkMzczZDQ2NjllMjlkMzZiOTZlMGQyNzUxZWJkZDc5In0.ptvHYSs-3yeWx5pY3FG0HIQwZ1wNadpt1ps0fhzkdlk"

echo "Test 1: Missing transaction.id"
curl -s -X POST https://sandbox.smartfastpay.com/v2/transaction/checkout \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d "{
       \"customer\": { \"id\": \"cust_$(date +%s)_1\", \"name\": \"John Doe\", \"email\": \"john.doe@example.com\", \"document\": { \"number\": \"A12345678\", \"type\": \"PA\" } },
       \"transaction\": { \"currency\": \"USD\", \"amount\": 10.00 },
       \"country\": \"ECU\",
       \"payment_method\": [\"bank_transfer\"],
       \"notification_url\": \"http://localhost:8000/webhook\"
     }"
echo -e "\n---"

echo "Test 2: Invalid Data Type (amount as string)"
curl -s -X POST https://sandbox.smartfastpay.com/v2/transaction/checkout \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d "{
       \"customer\": { \"id\": \"cust_$(date +%s)_2\", \"name\": \"John Doe\", \"email\": \"john.doe@example.com\", \"document\": { \"number\": \"A12345678\", \"type\": \"PA\" } },
       \"transaction\": { \"id\": \"trans_$(date +%s)_2\", \"currency\": \"USD\", \"amount\": \"10.00\" },
       \"country\": \"ECU\",
       \"payment_method\": [\"bank_transfer\"],
       \"notification_url\": \"http://localhost:8000/webhook\"
     }"
echo -e "\n---"

echo "Test 3: Invalid Country (XYZ)"
curl -s -X POST https://sandbox.smartfastpay.com/v2/transaction/checkout \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $TOKEN" \
     -d "{
       \"customer\": { \"id\": \"cust_$(date +%s)_3\", \"name\": \"John Doe\", \"email\": \"john.doe@example.com\", \"document\": { \"number\": \"A12345678\", \"type\": \"PA\" } },
       \"transaction\": { \"id\": \"trans_$(date +%s)_3\", \"currency\": \"USD\", \"amount\": 10.00 },
       \"country\": \"XYZ\",
       \"payment_method\": [\"bank_transfer\"],
       \"notification_url\": \"http://localhost:8000/webhook\"
     }"
echo -e "\n---"
