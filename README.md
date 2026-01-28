# PRD Assistant - Payment Integration Workflow System

A systematic approach to payment provider integrations using **Antigravity** with PRD-First methodology.

## Overview
This project handles 3-4 payment provider integrations daily using a standardized, phase-based workflow. Built for **Jupyter Notebook-style execution** where you can run individual steps, iterate until satisfied, or execute entire phases at once.

## Quick Start

### 1. Create New Integration
```bash
# Copy the template
cp -r integrations/_TEMPLATE integrations/Integration_ProviderName_Country_Currency_Method

# Example: Integration_SmartFastPay_Ecuador_USD_PayinHPP
```

### 2. Prepare Integration Folder
```bash
cd integrations/Integration_ProviderName_...

# Add provider docs and Epic requirements to 0_initial_docs/
# Fill in the config file with credentials and API URLs
```

### 3. Execute Research Phase
Open the integration folder in Antigravity and run:

**Option A: Step-by-step** (iterative, Jupyter-style)
```
/step1-epic-analysis
[Review output, re-run if needed]

/step2-docs-analysis
[Review output, re-run if needed]

/step3-test-page
[Review output, test manually, re-run if needed]

... continue through step7
```

**Option B: Full phase** (automated)
```
/phase1-full
[Agent executes all 7 steps, confirms between steps]
```

## Project Structure

```
prd_assistant/
├── .gemini.md                    # Global rules (auto-loaded by Antigravity)
├── .agent/
│   ├── skills/
│   │   └── test_page_generator/  # Auto-triggered for Step 3
│   └── workflows/
│       ├── phase1-full.md        # /phase1-full
│       ├── step1-epic-analysis.md
│       ├── step2-docs-analysis.md
│       ├── step3-test-page.md
│       ├── step4-access-fields.md
│       ├── step5-compatibility.md
│       ├── step6-project-stories.md
│       └── step7-field-testing.md
├── app/                      # Centralized helper apps
│   ├── serve.py              # Local testing server (CORS + Webhooks)
│   ├── webhook_viewer.html   # Webhook Visualization UI
│   └── serve.log             # Server logs
├── global_rules/
│   └── master_prd.yaml           # PRD schema definition
├── integrations/
│   ├── _TEMPLATE/                # Template for new integrations
│   └── Integration_<Name>/       # Actual integration workspaces
│       ├── 0_initial_docs/       # Epic, provider docs (immutable)
│       ├── 1_research/           # Phase 1 outputs (7 files)
│       ├── 2_development/        # Phase 2 outputs
│       ├── 4_test/               # Phase 4 QA outputs
│       ├── config                # API credentials, URLs
│       └── project_rules.md      # Optional: integration-specific overrides
└── _archive/                     # Deprecated: old instruction files
```

## Workflow Details & Commands

### Phase 1: Research
**Goal**: Complete deep analysis and fill all necessary stories before writing code.
**Command**: `/phase1-full` (Run all steps) or run individually below.
**Output Directory**: `1_research/`

#### Step 1: Epic Analysis
**Command**: `/step1-epic-analysis`
**File**: `1_research/1.epic_analysis.md`
*   **Action**: Evaluate the completeness of the Epic description (e.g., Jira link).
*   **Content**:
    *   Summary of requirements.
    *   Identification of unclear points.
    *   List of questions for the Product Owner (PO).

#### Step 2: Documentation Analysis
**Command**: `/step2-docs-analysis`
**File**: `1_research/2.docs_analysis.md`
*   **Action**: Deep dive into the provider's documentation.
*   **Content**:
    *   Links to official docs.
    *   Authentication method analysis.
    *   List of available payment methods and restrictions.

#### Step 3: Local Test Page
**Command**: `/step3-test-page`
**File**: `1_research/3.local_test_page.md`
*   **Action**: Create a functional HTML test page in file `1_research/3.test_page.html` to verify API behavior physically.
*   **Instructions**:
    1.  Populate the `config` file with `PROVIDER_API_DOCUMENTATION_URL`, `TEST_POST_WEBHOOK_URL`, `TEST_GET_WEBHOOK_URL`.
    2.  Use the test page generator skill (or run slash command).
*   **Content**:
    *   The generated HTML file (embedded or linked).
    *   Screenshots/Logs of a successful transaction created via this page.

#### Step 4: Access & Field Verification
**Command**: `/step4-access-fields`
**File**: `1_research/4.access_and_fields.md`
*   **Action**:
    *   Verify credentials (login to portal, API keys).
    *   Compare `service.fields` required for transaction creation against the documentation.
*   **Content**:
    *   Status of access (Ready/Pending).
    *   Table comparing "Requested Fields" vs "Actual Provider Fields".

#### Step 5: Compatibility Check
**Command**: `/step5-compatibility`
**File**: `1_research/5.compatibility.md`
*   **Action**: Check if the new method is compatible with the current system architecture.
*   **Content**:
    *   Flag any blocking architectural mismatches.
    *   Confirm if standard flow applies or if custom logic is needed.

#### Step 6: Fill Project Stories
**Command**: `/step6-project-stories`
**File**: `1_research/6.project_stories.md`
*   **Action**: Fill in the technical details for the standard set of stories.
*   **Content Sections**:
    1.  **Authorization**: How to authenticate (Headers, Token, Signature).
    2.  **Create Transaction Request**: Full payload example with mappings.
    3.  **Create Transaction Response**: Expected success/error response parsing.
    4.  **Callback (Webhook)**: Structure of the notification, validation logic (signature check), and response acknowledgment.
    5.  **Check Status**: Endpoint to poll status if callbacks fail.
    6.  **Final Statuses**: Mapping of Provider Statuses → Internal Statuses.
    7.  **Error Mapping**: Table of Provider Error Codes → Internal User Messages.

#### Step 7: Field Testing
**Command**: `/step7-field-testing`
**File**: `1_research/7.field_testing.md`
*   **Action**: Test edge cases and specific field handling.
*   **Content**:
    *   **International Format**: Phone number validation.
    *   **Transliteration**: Cyrillic/Special char acceptance.
    *   **Amount Handling**: Cents vs Integers.
    *   **Tester Specifics**: QA verification values.

### Phase 2: Development
**Goal**: Implement the logic defined in Phase 1.
**Output Directory**: `2_development/`

#### Step 8: Balance Retrieval
**File**: `2_development/8.balance_retrieval.md`
*   **Action**: Describe the method for obtaining account balances.
*   **Content**:
    *   Endpoint URL.
    *   Request/Response structure.
    *   Frequency limits.

### Phase 4: Testing
**Goal**: Integration Verification.
**Output Directory**: `4_test/`

*   Place all QA reports, automated test scripts (Python/Postman), and final sign-off documents here.
*   Follow the standard validation checklist (Happy Path, Error Cases, Timeout handling).

## Key Features

### 🎯 Jupyter Notebook Execution Style
- Execute individual steps and review results
- Re-run specific steps until results are satisfactory
- Full control over iteration speed

### 🤖 Antigravity Native Configuration
- **Rules**: `.gemini.md` loaded automatically (no manual prompting)
- **Skills**: Auto-triggered by context (e.g., test page generation)
- **Workflows**: Slash commands for step-by-step execution

### 📋 PRD-First Methodology
All integrations follow the **Hierarchy of Truth**:
1. Integration-specific `project_rules.md` (highest priority)
2. BetterBro standards
3. Master PRD schema
4. Provider documentation (validated via testing)

### 🔄 Template-Based Workflow
Create 3-4 integrations daily from standardized template:
- Consistent folder structure
- Pre-configured config file
- Ready-to-use workflows

## Global Rules

### BetterBro Standards
- H2H preferred over Redirects
- PIX = dynamic QR codes
- Webhooks must be authenticated
- Field mapping follows BetterBro schema

### Working Directory Isolation
- Research Agent → `1_research/` only
- Development Agent → `2_development/` only
- Test Agent → `4_test/` only

### Configuration Files
Every integration has:
- `config`: API credentials, documentation URL.
- `project_rules.md` (optional): Integration-specific overrides

### Centralized App (`app/`)
Contains utility tools to support testing across all integrations:
- **`serve.py`**: A unified local server that handles:
    - **CORS Proxy**: `POST /proxy`
    - **Webhook Ingestion**: `POST /webhook`
    - **API**: `GET/DELETE /api/webhooks`
- **`webhook_viewer.html`**: A modern UI for viewing caught webhooks.

**Usage**:
The workflows (e.g., `/step3-test-page`) automatically manage this server.
To run manually:
```bash
# From repository root
nohup python3 app/serve.py > /dev/null 2>&1 &
```
- Webhook Viewer: [http://localhost:8000/webhook_viewer.html](http://localhost:8000/webhook_viewer.html)
- Webhook Ingest URL: `http://localhost:8000/webhook`

## Skills

### test_page_generator
Auto-triggered during Step 3 or when user mentions "create test page".

**Generates**:
- Functional HTML test page with credential input
- Token generation and transaction creation
- Webhook polling and display
- Request/response logging

**Output**:
- `3.test_page.html`
- `3.local_test_page.md` (with usage instructions)


## Tips

### Creating New Integrations
1. Always copy from `_TEMPLATE`, don't create from scratch
2. Fill `config` before starting workflows
3. Populate `0_initial_docs/` with Epic and provider docs

### Iterative Refinement
```
You: /step2-docs-analysis
Agent: [Creates 2.docs_analysis.md]

You: The authentication section is incomplete, re-run step 2
Agent: [Re-runs step 2 with more detail]

You: Perfect! /step3-test-page
```

### Custom Rules
If an integration needs special handling:
1. Create `project_rules.md` in that integration folder
2. Document the override (e.g., "Skip webhook testing")
3. Rules apply only to that integration

### Parallel Agent Work (Advanced)
Use Antigravity's Agent Manager to:
- Set up multiple integrations in parallel
- Run different phases concurrently
- Batch process similar providers

## Support
For questions about:
- **BetterBro Standards**: See `.gemini.md` → BetterBro Standards section
- **Workflow Steps**: Read individual workflow files in `.agent/workflows/`
- **Skills**: Check `.agent/skills/<skill-name>/SKILL.md`
- **Master PRD Schema**: See `global_rules/master_prd.yaml`
