---
description: Execute all 7 steps of Phase 1 Research sequentially
---

# Phase 1: Complete Research Flow

Executes all research steps for the current integration in the `1_research/` folder.

## Prerequisites
- Integration folder must exist in `/integrations/<Integration_Name>/`
- `0_initial_docs/` must contain provider documentation and Epic/Jira requirements
- `config` file must have API credentials and documentation URL filled in

## Execution Pattern
This workflow runs all 7 research steps in sequence:
1. Epic Analysis
2. Documentation Analysis
3. Local Test Page (triggers `test_page_generator` skill)
4. Access & Field Verification
5. Compatibility Check
6. Fill Project Stories
7. Field Testing

**User Control**: After each step completes, confirm with the user before proceeding to the next step unless all steps were explicitly requested at once.

## Steps

### Step 1: Epic Analysis
Read Epic/Jira requirements from `0_initial_docs/` and create `1_research/1.epic_analysis.md` with:
- Summary of payment method, countries, flow type
- List of requirements
- Unclear points and questions for Product Owner

### Step 2: Documentation Analysis
Deep dive into provider's API documentation and create `1_research/2.docs_analysis.md` with:
- Links to official docs
- Authentication method analysis
- Available payment methods and restrictions
- API endpoint inventory

### Step 3: Local Test Page (Split)
Execute the following two steps:

**Step 3a: Create Test Page**
Invoke the `step3a-create-test-page` workflow (which uses `test_page_generator` skill) to create:
- `1_research/3.test_page.html` - Functional test page
- `1_research/3.test_page.md` - Documentation with usage instructions

**Step 3b: Auto Test Page**
Invoke the `step3b-auto-test-page` workflow to:
- Automatically test the page with a browser agent
- Fix issues if found
- Update `1_research/3.test_page.md` with test results

### Step 4: Access & Field Verification
Verify credentials and create `1_research/4.access_and_fields.md` with:
- Status of access (Ready/Pending)
- Table comparing "Requested Fields" vs "Actual Provider Fields"
- Login verification results

### Step 5: Compatibility Check
Check system compatibility and create `1_research/5.compatibility.md` with:
- Architectural compatibility assessment
- Flag any blocking mismatches
- Confirmation if standard flow applies or custom logic needed

### Step 6: Fill Project Stories
Create technical specifications in `1_research/6.project_stories.md` with:
1. **Authorization**: Authentication method (Headers, Token, Signature)
2. **Create Transaction Request**: Full payload example with field mappings
3. **Create Transaction Response**: Expected success/error response parsing
4. **Callback (Webhook)**: Notification structure, validation logic, acknowledgment
5. **Check Status**: Endpoint to poll status if callbacks fail
6. **Final Statuses**: Provider Status → Internal Status mapping
7. **Error Mapping**: Provider Error Codes → Internal User Messages

### Step 7: Field Testing
Test edge cases and create `1_research/7.field_testing.md` with:
- **International Format**: Phone number/ID validation (e.g., +380 vs 380)
- **Transliteration**: Cyrillic/Special character support
- **Amount Handling**: Cents vs Integers (10.00 vs 1000)
- **Tester Specifics**: QA-provided test values

## Success Criteria
All 7 files created in `1_research/` folder with complete, accurate information ready for Phase 2 development.

## Output Directory
`<current_integration>/1_research/`
