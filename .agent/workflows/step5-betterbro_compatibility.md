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
    -   **Step B: Active Web Search (Validation)**:
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

3.  **Field Mapping Analysis**:
    -   Review `2.docs_analysis.md` and `4.auto_test_page.md`.
    -   Verify that every mandatory request field from the Provider has a corresponding standard field in the BetterBro internal schema for the selected **Rule**.
    -   Verify that every response field (synchronous or webhook) can be mapped to a standard internal field.

4.  **Status Mapping Analysis**:
    -   Identify all possible transaction statuses from the Provider.
    -   Map each one to a 4bill internal status (e.g., `1 SUCCESS`, `2 FAILED`, `3 PENDING`, `4 REFUNDED`, `5 CHARGEBACK`).
    -   **CRITICAL**: If a status is ambiguous, mark it as a RISK.

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

## User Confirmation
"BetterBro validation complete. Review `5.betterbro_compatibility.md`. Does this integration fit our 'internal language'?"