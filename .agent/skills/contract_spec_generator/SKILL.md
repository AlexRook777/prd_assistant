---
name: Contract Spec Generator
description: Generates a machine-executable OpenAPI 3.1 specification (Step 7) from human-readable PRD artifacts (Steps 1-6).
---

# Contract Spec Generator Skill

This skill synthesizes the "Human Truth" found in PRD documents (Steps 1-6) into a "Machine Truth" executable contract (Step 7). It produces a strictly typed OpenAPI 3.1 YAML file enriched with custom extensions for internal mapping compatibility.

## Input Artifacts

Run this skill ONLY after completing Steps 1-6. It requires the following inputs from `<current_integration>/1_result/`:

1.  `2.docs_analysis.md` (Endpoints, Auth methods)
2.  `4.auto_test_page.md` (Verified Webhook schemas, accurate request/response examples)
3.  `5.betterbro_compatibility.md` (Field Mappings, Status Mappings, Architecture Type)
4.  `6.project_stories.md` (Business Logic context)

## Output Artifacts

1.  `7.contract_spec.yaml` (The OpenAPI 3.1 Specification)
2.  `7.contract_spec.md` (Human-readable summary)
3.  `handoff_package.zip` (Final delivery package)

## Process

### 1. Initialize Specification

*   Load `templates/openapi_base.yaml`.
*   Update `info` object:
    *   `title`: Integration Name (from `1.epic_analysis.md`)
    *   `version`: 1.0.0
    *   `x-4bill-metadata`: Populate from `5.betterbro_compatibility.md` (Provider, Region, Type).

### 2. Define Endpoints (from `2.docs_analysis.md` & `4.auto_test_page.md`)

*   **Identify** all endpoints used in the integration.
*   **Method**: GET/POST/PUT etc.
*   **Path**: The relative path (e.g., `/v1/payments`).
*   **Security**: Apply the auth scheme identified in Step 2.

### 3. Generate Schemas (The "Type Safety" Step)

*   **Request Body**:
    *   Use examples from `4.auto_test_page.md` (actual successful payloads).
    *   Convert JSON to JSON Schema.
    *   **CRITICAL**: Enforce required fields.
*   **Response Body**:
    *   Use simple success/error examples from logs.

### 4. Apply BetterBro Mappings (from `5.betterbro_compatibility.md`)

*   **Field Mapping**:
    *   Iterate through the *Field Mapping Table* in Step 5.
    *   For each mapped field in the Request Schema, add the `x-betterbro-mapping` extension.
    *   Example:
        ```yaml
        customer_email:
          type: string
          format: email
          x-betterbro-mapping:
            field: "customer.email"
            required: true
        ```

*   **Status Mapping**:
    *   Locate the `status` field in the Response Schema or Webhook Schema.
    *   Add the `x-betterbro-status-codes` extension using the *Status Mapping Table* from Step 5.
    *   Example:
        ```yaml
        status:
          type: string
          enum: [PAID, FAILED, PENDING]
          x-betterbro-status-codes:
            PAID: 1
            FAILED: 2
            PENDING: 3
        ```

### 5. Define Webhooks (from `4.auto_test_page.md`)

*   **Path**: Define the webhook receiver path (usually `/webhook` or callback URL).
*   **Payload**: Use the *verified* webhook JSON content from Step 4.
*   **Signature**: Document the signature header (e.g., `X-Signature`) in parameters.

### 6. Validation

*   **Linting**: Ensure the YAML is valid OpenAPI 3.1.
*   **Check Mappings**: Verify that every mandatory BetterBro field has a corresponding mapped field in the spec.

## Instructions for the Agent

1.  **Read** all input files first to build context.
2.  **Draft** the YAML in memory.
3.  **Refine** schemas by looking at actual JSON logs in `4.auto_test_page.md`.
4.  **Inject** existing `x-betterbro-*` extensions from `templates/betterbro_extensions.yaml` if defining common types.
5.  **Write** the final `7.contract_spec.yaml`.
6.  **Create** the ZIP package containing `1_result/*.md` and the new YAML.
