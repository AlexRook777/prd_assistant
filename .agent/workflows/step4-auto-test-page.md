---
description: Phase 1 Step 3b - Automate test page verification and fixing
---

# Step 3b: Automate Test Page

Automatically test the generated `3.test_page.html` using a browser agent. If issues are found, the agent will attempt to fix the HTML file and retry.

## Working Directory
`<current_integration>/1_result/`

## Prerequisites
- `3.test_page.html` must exist (Run Step 3a first).
- `serve.py` must be running (The workflow handles this).

## Task

1. **Ensure Server is Running**:
   - **Check**: Is port 8000 occupied?
   - **Linux**: `fuser -k 8000/tcp` followed by `nohup python3 app/serve.py > /dev/null 2>&1 &` (run from repo root)
   - **Mac**: `lsof -ti:8000 | xargs kill -9` followed by `nohup python3 app/serve.py > /dev/null 2>&1 &`
   - **Windows**: `taskkill /F /IM python.exe /T` (to kill) -> `start /B python app/serve.py`
   - **WAIT** 2 seconds for server to start.

2. **Loop: Test & fix**:
   - **Goal**: Successfully create a transaction and verify status.
   - **Action**:
         - Use `open_browser` to navigate to `http://localhost:8000/integrations/<Integration_Name>/1_result/3.test_page.html`.
         - Fill in credentials from `config`.
         - Click "Get Token" (if applicable).
         - Click "Create Transaction".
         - **Verify**: Did it succeed?
           - **YES**: 
             - Take screenshot.
             - Create `1_result/4.auto_test_page.md` with a **Detailed Test Log**:
               - **General Status**: Success/Fail.
               - **Step-by-Step Log**: Detailed actions and results for Token, Transaction, and Webhook.
               - **Issues & Fixes**: List any issues encountered, what caused them, and how they were fixed.
               - **Workflow Suggestions**: Suggest improvements for future phases based on findings.
               - **Screenshots**: Embed successful transaction screenshots.
             - Stop.
       - **NO**:
         - Analyse the error (Console logs, UI error message).
         - **Fix**: Edit `3.test_page.html` to correct the issue (e.g., incorrect field name, missing header, wrong JSON format).
         - **Retry**: Reload page and try again.
         - **Limit**: Max 5 fix attempts. If still failing, create `1_result/4.auto_test_page.md` with "Issues Found" section and Stop.

3. **Output**:
   - Updated `3.test_page.html` (if fixes were needed).
   - Created `4.auto_test_page.md` with test results and screenshots.

## Success Criteria
- `4.auto_test_page.md` is created and contains a "Test Results" section.