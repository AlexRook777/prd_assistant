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

2.  **Read Documentation** (Comprehensive Research):
    -   Review the provider's API documentation (URL in `integration_config`) and any PDFs in `0_initial_docs_and_config/`.
    -   **Research and document the following**:
        -   **Authentication Method**: How does the provider authenticate requests? (OAuth 2.0, API Key, Basic Auth, etc.)
            -   Token endpoint and required credentials
            -   Token lifetime and refresh mechanism
            -   Required headers for authenticated requests
        -   **Transaction Initiation**: How is a payment transaction created?
            -   Correct API endpoint URL for transaction creation
            -   HTTP method (POST, PUT, etc.)
            -   Request format (JSON, form-urlencoded, etc.)
        -   **Expected Results**: What does a successful transaction creation return?
            -   Response structure and status codes
            -   Transaction ID format and location in response
            -   Any redirect URLs or next steps
        -   **Data Structure**: What fields are used in transaction requests?
            -   **Create a Table**: You **MUST** document these in a table format with columns: `Field`, `Type`, `Required?`, `Description`.
            -   **Ordering Rule**: You **MUST** list all **Mandatory (Yes)** fields first, followed by **Optional** fields.
            -   **Content**:
                -   **Mandatory fields**: Required parameters that must be present.
                -   **Optional fields**: Parameters that can be omitted or have defaults.
                -   Field types, formats, and validation rules.
                -   Nested object structures (customer, billing, etc.).
                -   **Step 7 Requirement**: This table will be the source for the `properties` map in the OpenAPI spec. Ensure types (string, integer, boolean) are accurate.
        -   **Payment URL Response**: How is the payment URL provided?
            -   Where in the response is the payment/checkout URL?
            -   URL format and structure
            -   URL lifetime and expiration
        -   **Callbacks (Webhooks)**: How does the provider notify about transaction updates?
            -   Webhook endpoint configuration
            -   Callback payload structure
            -   Authentication/signature verification method
            -   Retry policy and failure handling
        -   **Status Sets**: What are all possible transaction statuses?
            -   Complete list of status values
            -   Status transitions and flow
            -   Final states (success, failure, etc.)
            -   Any intermediate or pending states

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
    -   **Webhook Verification (N8n)**:
        -   Use the **N8n Webhook Tester** skill (`.agent/skills/n8n_webhook_tester/SKILL.md`).
        -   Generate a unique order ID for webhook testing.
        -   Include the n8n webhook URL in your transaction creation request.
        -   After transaction creation, poll for webhooks using the n8n retrieve endpoint.
        -   Document the webhook payload(s) in the "Webhook Verification" section of `2.docs_analysis.md`.
        -   See the skill documentation for curl examples and usage patterns.

4.  **Present Payment Link** (API Verification Result):
    -   **Extract the Payment URL**: From the successful transaction creation in step 3, identify and extract the payment/checkout URL from the API response.
    -   **Document Clearly**: Add a dedicated section in `2.docs_analysis.md` titled "**Live Payment Link (Verification)**" that includes:
        -   The complete payment URL obtained from the test transaction
        -   The transaction ID associated with this payment link
        -   Timestamp of when the link was generated
        -   Link expiration time (if applicable)
        -   Instructions on how to test the payment flow manually
    -   **Format Example**:
        ```markdown
        ## Live Payment Link (Verification)
        
        **Generated**: 2026-02-04 14:22:00 UTC
        **Transaction ID**: TXN123456789
        **Payment URL**: https://checkout.provider.com/pay/abc123def456
        **Expires**: 2026-02-05 14:22:00 UTC (24 hours)
        
        ### Testing Instructions
        1. Open the payment URL in a browser
        2. Complete the payment flow using test card credentials
        3. Verify the redirect to success/failure URL
        4. Check webhook callback reception (if configured)
        ```
    -   **Highlight**: This payment link proves that the integration can successfully create transactions and generate payment URLs.

5.  **Final Review**:
    -   Ensure the generated `2.docs_analysis.md` follows the format defined in the Skill.
    -   Verify that it contains *real* `curl` output, not just documentation copies.
    -   Confirm that the **Live Payment Link** section is present and clearly visible.

6. **Include Workflow Suggestions**: End the file with `## Workflow Suggestions` section (see `.gemini.md` for format).