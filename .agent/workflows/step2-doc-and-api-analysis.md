---
description: Phase 1 Step 2 - Analyze provider's API documentation with active verification
---

# Step 2: Documentation & API Verification

This step performs a deep dive into the payment provider's API documentation and uses the **API Verification Skill** to actively test the endpoints.

## Working Directory
`<current_integration>/1_result/`

## Output File
`2.docs_analysis.md`

## Prerequisites
- `integration_config` file must have `PROVIDER_API_DOCUMENTATION_URL`, `CLIENT_ID`, and `CLIENT_SECRET` filled in.
- You must have Internet access to reach the Provider's Sandbox environment.

## Task

1.  **Reference Check**:
    -   Check if `2.docs_analysis.md` already exists. If so, read it to preserve any clarified points or user feedback.

2.  **Read Documentation**:
    -   Review the provider's API documentation (URL in `integration_config`) and any PDFs in `0_initial_docs_and_config/`.

3.  **Execute API Verification Skill**:
    -   Use the **API Verification Report** skill (`.agent/skills/api_verification_report/SKILL.md`).
    -   **Context**:
        -   Use credentials from the local `integration_config`.
        -   Target the Sandbox environment.
        -   Focus on the "Payin" or "Checkout" flow relevant to this integration.
    -   **Output**: Save the generated report to `2.docs_analysis.md`.
    -   **Action**: Follow the skill's instructions to:
        -   Verify Authentication.
        -   Provide a "Happy Path" transaction creation example.
        -   Run "Negative Tests" (Validation) to find error codes.
        -   Compile the "Discrepancy Table".

4.  **Final Review**:
    -   Ensure the generated `2.docs_analysis.md` follows the format defined in the Skill.
    -   Verify that it contains *real* `curl` output, not just documentation copies.