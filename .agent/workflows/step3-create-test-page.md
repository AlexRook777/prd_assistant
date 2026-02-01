---
description: Phase 1 Step 3a - Create functional HTML test page for API verification
---

# Step 3a: Create Test Page

Create a functional HTML test page to physically verify the payment provider's API behavior and test webhooks. This step handles only the **generation** of the page. Step 3b handles the automated testing.

## Working Directory
`<current_integration>/1_research/`

## Output Files
- `3.test_page.html` - Functional test page
- `3.test_page.md` - Documentation and test results (partially filled)

## Prerequisites
- `config` file must have:
  - `PROVIDER_API_DOCUMENTATION_URL`
  - We use the local `serve.py` which provides `http://localhost:8000/webhook`.

## Task

1. **Pre-computation Check**:
   - Check if `3.test_page.md` already exists.
   - **IF IT EXISTS**:
     - Read the file content.
     - Extract **Test Results** (Token status, Transaction IDs, Screenshots) from previous runs (if any).
     - Extract **Issues Found**.
     - **Preserve** these details in the new report.
   - **IF IT DOES NOT EXIST**: Proceed normally.

2. This step **automatically invokes** the `test_page_generator` skill. The skill will:
   - Read the provider's API documentation
   - **Read `1_research/2.docs_analysis.md`** for comprehensive field list and requirements.
   - Read the `config` file for API details
   - **Generate a functional HTML test page** (`3.test_page.html`) that **INCLUDES** the Webhook Viewer UI.
   - Create documentation (`3.test_page.md`) with usage instructions.

## Success Criteria
- `3.test_page.html` created and functional
- `3.test_page.md` created with usage instructions

## Next Steps
- Run `/step4-auto-test-page` to automatically test the page with a browser agent.