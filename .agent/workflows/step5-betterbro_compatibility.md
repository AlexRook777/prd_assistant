---
description: Phase 1 Step 5 - Check compatibility with system architecture and BetterBro standards
---

# Step 5: BetterBro Protocol Alignment & Feasibility

**Goal**: Validate that the provider's integration can be fully normalized into the "BetterBro" 4bill internal standard. This ensures that every field has a home and every status corresponds to a 4bill internal code, enabling full automation.

## Working Directory
`<current_integration>/1_result/`

## Output File
`5.betterbro_compatibility.md`

## Task



1.  **Pre-computation Check**:
    -   Check if `5.betterbro_compatibility.md` already exists.
    -   **IF IT EXISTS**: Read it and preserve any manual "Blocking Issues" or "Custom Logic" notes.

2.  **Rule Identification (Crucial)**:
    -   **Step A: Check Epic/Input**:
        -   Review `1.epic_analysis.md` for a provided **BetterBro Service Rule** OR **BetterBro Service URL**.
        -   **IF PROVIDED**: Use it to identify the Rule (derive from URL if needed), treat it as a *Draft Result*, and validate if it aligns with the provider's capabilities.
    -   **Step B: Active Web Search (Discovery)**:
        -   **Action**: Perform a web search to confirm the correct "BetterBro Service URL" and "Rule" if not absolutely certain.
        -   **Queries**:
            -   `"BetterBro" [Service Rule] documentation`
            -   `"BetterBro" [Payment Method] integration guide`
            -   `[Provider Name] BetterBro compatibility`
        -   **Goal**: Find a specific URL like `https://docs.betterbro.com/services/...` that matches the mapped rule.
    -   **Step C: Manual Identification (Fallback)**:
        -   **IF NOT PROVIDED** in Epic OR **NOT VALID/ALIGNED**:
        -   Consult the [BetterBro Services Documentation](https://docs.betterbro.com/).
        -   Identify which **BetterBro Service Rule** fits the provider's integration type.
    -   **Common Rules**:
        -   `Acquiring Form` (HPP / Checkout Page)
        -   `Acquiring H2H` (S2S / API-based)
        -   `Card Tokenization` (Vaulting)
        -   `Card Payouts` (Disbursements)
    -   **Action**: Explicitly state which Rule applies.
    -   **Service Identification**: Include the specific "Service Instance" name, the "Service URL" from the provider docs, and the "BetterBro Service URL" from the internal docs.
    -   **Step D: Download BetterBro Specification (NEW - Deep Analysis)**:
        -   **Action**: Once the correct BetterBro Service URL is identified, use the browser to navigate to that page.
        -   **View Page as Markdown**: Click the menu (⋮) → "View page as Markdown" to open the content in a new tab.
        -   **Save Location**: Copy the displayed markdown content and save it as `betterbro_service_spec.md` in the `<current_integration>/0_initial_docs_and_config/` directory.
        -   **CRITICAL**: The saved markdown file is the SOURCE OF TRUTH. Do NOT re-read the URL with `read_url_content` as it may return generic/root page content instead of the specific service documentation.
        -   **Purpose**: This provides the complete, structured specification for comprehensive field mapping and status code analysis.
    -   **Step E: Verify File (Validation)**:
        -   **Action**: Check that `betterbro_service_spec.md` exists in the `0_initial_docs_and_config/` directory.
        -   **Validation**: Open the file and verify it contains service-specific content (field mappings, status codes, regional requirements) and NOT generic introduction text.
        -   **Fallback**: If the capture failed, the file is missing, or it contains only generic content:
            -   Manually create `betterbro_service_spec.md` based on web search results and BetterBro documentation.
            -   Document the standard Acquiring Form (HPP) field mappings and status codes.
            -   Include regional requirements if applicable (e.g., Ecuador document fields).

3.  **Field Mapping Analysis**:
    -   Review `2.docs_analysis.md` and `4.auto_test_page.md` for provider field requirements.
    -   Review the **saved** `<current_integration>/0_initial_docs_and_config/betterbro_service_spec.md` for the complete BetterBro field specification.
    -   **IMPORTANT**: Use ONLY the saved markdown file, not the live URL.
    -   **Cross-Reference**: Compare provider fields against BetterBro standard fields from the downloaded specification.
    -   Verify that every mandatory request field from the Provider has a corresponding standard field in the BetterBro internal schema for the selected **Rule**.
    -   Verify that every response field (synchronous or webhook) can be mapped to a standard internal field.
    -   **Parse Tables**: Extract field mapping tables, data type requirements, and validation rules from the BetterBro spec.

4.  **Status Mapping Analysis**:
    -   Identify all possible transaction statuses from the Provider (from `2.docs_analysis.md`).
    -   Review status code definitions in the **saved** `<current_integration>/0_initial_docs_and_config/betterbro_service_spec.md`.
    -   **IMPORTANT**: Use ONLY the saved markdown file for status mapping reference.
    -   Map each provider status to a 4bill internal status (e.g., `1 SUCCESS`, `2 FAILED`, `3 PENDING`, `4 REFUNDED`, `5 CHARGEBACK`).
    -   **CRITICAL**: If a status is ambiguous or doesn't have a clear BetterBro equivalent, mark it as a RISK.

5.  **Automation Feasibility**:
    -   Confirm the flow is deterministic (Rulebook compliant).
    -   Can AI agents automatically determine the outcome based *only* on the documentation rules?

6.  **Create Documentation**:

```markdown
# BetterBro Compatibility Report

**Date**: [Current Date]

## 1. Rulebook Identification
- **Selected Rule**: [e.g. Acquiring Form / H2H / Payouts]
- **Service Instance**: [Specific Service Name from docs, e.g. Ecuador Bank Transfer Payin HPP]
- **Provider  Service URL**: [Link to provider service documentation]
- **BetterBro Service URL**: [Link to BetterBro service documentation]
- **Confidence**: [High / Medium / Low]
- **Rationale**: [Why this rule fits the best]

## 2. Field Mapping Feasibility
| Provider Field | BetterBro Standard Field | Notes |
| :--- | :--- | :--- |
| `example_field` | `transaction.description` | Direct match |
| `custom_data` | `metadata` | Mapped to generic metadata |
| `unique_id` | `transaction.id` | |

**Missing Fields**:
- [List any provider fields that do NOT have a clear internal mapping]

## 3. Status Mapping (The "Rosetta Stone")
| Provider Status | 4bill Internal Code | Logic/Rule |
| :--- | :--- | :--- |
| `AUTHORIZED` | `1 SUCCESS` | Immediate success |
| `DECLINED` | `2 FAILED` | Final failure |
| `WAITING` | `3 PENDING` | Async flow |

**Ambiguous Statuses**:
- [List any statuses that are hard to map]

## 4. Automation & Logic
- **Architecture Type**: [HPP / Redirect / H2H]
- **Deterministic**: [Yes / No]
- **Webhooks**: [Standard HMAC / ID Verification / None]

## 5. Blocking Issues & Risks
- [CRITICAL] [Description of any blocker]
- [RISK] [Description of potential friction]

## 6. Recommendation
- [ ] **GREEN LIGHT**: Fully compatible, proceed to implementation.
- [ ] **YELLOW LIGHT**: Minor custom logic needed, proceed with caution.
- [ ] **RED LIGHT**: Major architectural blocker, STOP and discuss.

## Next Steps
- [ ] Proceed to Step 6 (Project Stories)
```

7. **Include Workflow Suggestions**: End the file with `## Workflow Suggestions` section (see `.gemini.md` for format).

## User Confirmation
"BetterBro validation complete. Review `5.betterbro_compatibility.md`. Does this integration fit our 'internal language'?"