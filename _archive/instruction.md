# Integration Process Instructions

This document acts as the **Single Source of Truth** for building new integrations. It defines the strict folder structure, required files, and the step-by-step process for specific phases.

## Project Structure
Every new integration must follow this standardized directory structure:

```text
/Integrations/ <Integration_Name>/
├── 0_initial_docs/      # Raw documentation from provider
├── 1_research/          # Output of Phase 1 (Research & Analysis)
├── 2_development/       # Output of Phase 2 (Techncial Design & Development)
├── 4_test/              # Output of Phase 4 (QA & Validation)
└── initial.md           # Entry point and general info
```

User instructions:
1. The approach of execution should be similar to Google Colab (Jupiter notebook) where user can execute only that part of the instructions that were asked by user. DO NOT execute next steps until user asks for it.
2. If user asks to execute next steps, execute them in order.
3. If user asks to execute previous steps, execute them in order.
4. If user asks to execute specific step, execute it.
5. If user asks to execute all steps, execute them in order.

## Phase 1: Research

**Goal**: Complete deep analysis and fill all necessary stories before writing code.
**Output Directory**: `1_research/`

### Step 1: Epic Analysis
**File**: `1_research/1.epic_analysis.md`
*   **Action**: Evaluate the completeness of the Epic description (e.g., Jira link).
*   **Content**:
    *   Summary of requirements.
    *   Identification of unclear points.
    *   List of questions for the Product Owner (PO).

### Step 2: Documentation Analysis
**File**: `1_research/2.docs_analysis.md`
*   **Action**: Deep dive into the provider's documentation.
*   **Content**:
    *   Links to official docs.
    *   Authentication method analysis.
    *   List of available payment methods and restrictions.

### Step 3: Local Test Page
**File**: `1_research/3.local_test_page.md`
*   **Action**: Create a functional HTML test page in file `1_research/3.test_page.html` to verify API behavior physically .
*   **Instructions**:
    1.  Populate the `config` file with:
        *   `PROVIDER_API_DOCUMENTATION_URL`
        *   `TEST_POST_WEBHOOK_URL`
        *   `TEST_GET_WEBHOOK_URL`
    2.  Use the prompt `global_prompts/1_test_page.md` to generate the HTML file.
*   **Content**:
    *   The generated HTML file (embedded or linked).
    *   Screenshots/Logs of a successful transaction created via this page.

### Step 4: Access & Field Verification
**File**: `1_research/4.access_and_fields.md`
*   **Action**:
    *   Verify credentials (login to portal, API keys).
    *   Compare `service.fields` required for transaction creation against the documentation.
*   **Content**:
    *   Status of access (Ready/Pending).
    *   Table comparing "Requested Fields" vs "Actual Provider Fields".

### Step 5: Compatibility Check
**File**: `1_research/5.compatibility.md`
*   **Action**: Check if the new method is compatible with the current system architecture.
*   **Content**:
    *   Flag any blocking architectural mismatches.
    *   Confirm if standard flow applies or if custom logic is needed.

### Step 6: Fill Project Stories
**File**: `1_research/6.project_stories.md`
*   **Action**: Fill in the technical details for the standard set of stories.
*   **Content Sections**:
    1.  **Authorization**: How to authenticate (Headers, Token, Signature).
    2.  **Create Transaction Request**: Full payload example with mappings.
    3.  **Create Transaction Response**: Expected success/error response parsing.
    4.  **Callback (Webhook)**: Structure of the notification, validation logic (signature check), and response acknowledgment (e.g., HTTP 200).
    5.  **Check Status**: Endpoint to poll status if callbacks fail.
    6.  **Final Statuses**: Mapping of Provider Statuses $\to$ Internal Statuses (Success, Fail, Pending).
    7.  **Error Mapping**: Table of Provider Error Codes $\to$ Internal User Messages.

### Step 7: Field Testing
**File**: `1_research/7.field_testing.md`
*   **Action**: Test edge cases and specific field handling.
*   **Content**:
    *   **International Format**: How phone numbers/IDs are validated (e.g., +380 vs 380).
    *   **Transliteration**: Does the provider accept Cyrillic/Special chars? (Test result: Yes/No).
    *   **Amount Handling**: Cents vs Integers (e.g., `10.00` vs `1000`).
    *   **Tester Specifics**: Specific values provided by QA that need verification.

---

## Phase 2: Development

**Goal**: Implement the logic defined in Phase 1.
**Output Directory**: `2_development/`

### Step 8: Balance Retrieval
**File**: `2_development/8.balance_retrieval.md`
*   **Action**: Describe the method for obtaining account balances.
*   **Content**:
    *   Endpoint URL.
    *   Request/Response structure.
    *   Frequency limits (if any).

---

## Phase 4: Testing

**Goal**: Integration Verification.
**Output Directory**: `4_test/`

*   Place all QA reports, automated test scripts (Python/Postman), and final sign-off documents here.
*   Follow the standard validation checklist (Happy Path, Error Cases, Timeout handling).

