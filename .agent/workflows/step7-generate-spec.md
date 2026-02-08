---
description: Phase 2 Step 7 - Generate machine-executable contract specification
---

# Step 7: Generate Contract Specification

**Goal**: Synthesize all PRD artifacts (Steps 1-6) into a strictly typed, machine-executable OpenAPI 3.1 specification. This acts as the "Contract" for the Code Agent.

## Working Directory
`<current_integration>/1_result/`

## Output Artifacts
*   `7.contract_spec.yaml`
*   `7.contract_spec.md`
*   `handoff_package.zip`

## Required Skill
*   [.agent/skills/contract_spec_generator/SKILL.md](.agent/skills/contract_spec_generator/SKILL.md)

## Task

1.  **Read the Skill**: Read and understand `.agent/skills/contract_spec_generator/SKILL.md`.

2.  **Pre-computation Check**:
    *   Check if `7.contract_spec.yaml` exists.
    *   **IF IT EXISTS**: Read it to understand the current state.
    *   **IF NOT**: Proceed to generation.

3.  **Execute Spec Generation**:
    *   Invoke the skill instructions.
    *   **Input**: `2.docs_analysis.md`, `4.auto_test_page.md`, `5.betterbro_compatibility.md`, `6.project_stories.md`.
    *   **Output**: `7.contract_spec.yaml` (Markdown-embedded YAML is NOT acceptable; it must be a valid file).

4.  **Validate**:
    *   Ensure all endpoints from Step 2 are present.
    *   Ensure all fields from Step 5 are mapped.
    *   Ensure all status codes from Step 5 are present.
    *   **Self-Correction**: If validation fails, update the YAML.

5.  **Create Handoff Package**:
    *   Create a ZIP file named `handoff_package.zip` containing:
        *   `prd/`: All files from `1_result/`.
        *   `spec/`: The generated `7.contract_spec.yaml`.
        *   `assets/`: Any images or screenshots in `1_result/`.

6.  **Include Workflow Suggestions**:
    *   The next step is usually handing off to the Implementation Agent.

## Success Criteria
*   `7.contract_spec.yaml` is valid OpenAPI 3.1.
*   `x-betterbro-mapping` exists for all critical fields.
*   `x-betterbro-status-codes` exists for transaction status.
*   `handoff_package.zip` is created and contains all context.

## User Confirmation
"Contract Specification generated. Verified field mappings and status codes. Ready for handoff to Implementation Agent?"
