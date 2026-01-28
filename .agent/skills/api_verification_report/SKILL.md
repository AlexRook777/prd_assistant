---
name: API Verification Report
description: Perform deep-dive API verification including active curl testing, validation of error cases, and discrepancy reporting.
---

# API Verification & Reporting Skill

This skill guides you through creating a high-quality API verification report (`2.docs_analysis.md`) by actively testing the provider's API against its documentation.

## Goal
To produce a comprehensive report that not only analyzes the static documentation but **Proves** how the API works by executing real requests and analyzing the differences.

## Prerequisites
-   You typically need `clientId`, `clientSecret` (or similar credentials) available in the workspace `config`.
-   You must be able to reach the Sandbox environment via `curl`.

## Execution Steps

### 1. Static Documentation Analysis
-   **Action**: Read the documentation to understand the theoretical flow.
-   **Extract**:
    -   Auth method & endpoints.
    -   Transaction creation parameters (Required vs Optional).
    -   Webhook structure & security (Signature).
-   **Clarify**: Note any specific "Clarified Points" or user constraints (e.g., "Chile only").

### 2. Active Authentication (The "Hello World")
-   **Action**: Construct and run a `curl` command to get an access token.
-   **Verify**: 
    -   Does it require specific headers?
    -   Does it answer 200 OK?
-   **Output**: Capture the *exact* request and response.

### 3. Transaction "Happy Path"
-   **Action**: Create a *valid* transaction using `curl`.
    -   Use dummy data (e.g., `customer.email="test@example.com"`).
    -   Ensure all "Required" fields from docs are present.
-   **Verify**:
    -   Does it return `200 OK` / `201 Created`?
    -   **CRITICAL**: Immediately check the status (GET /transaction/{id}). Does it match?

### 4. "Negative Testing" (Validation Rules)
Run at least **3 specific failure scenarios** to find real error codes:
1.  **Missing Required Field**: e.g., omit `customer.name`.
2.  **Invalid Data Type**: e.g., send `amount` as string `"100.00"` instead of number.
3.  **Business Logic Error**: e.g., `amount: -100`.

### 5. Discrepancy & Gap Analysis
Compare Doc Theory vs API Reality.
-   Did the API require a field listed as optional?
-   Did the API return a String where Int was promised?

## Report Output Format

Generates a report (filename specified by the caller) with the following structure:

```markdown
# Documentation Analysis

**Provider**: [Provider Name]
**Documentation URL**: [URL]
**Date**: [YYYY-MM-DD]

## Clarified Points (User Feedback)
- [List any specific constraints or user clarifications found in previous steps or provided context]

## Authentication
### Method
[e.g., OAuth 2.0 with Bearer Token]
### Token Generation
- **Endpoint**: \`POST https://...\`
- **Required Headers**: \`...\`
### Verification (MANDATORY)
Successfully verified. Obtained token using:
\`\`\`bash
[CURL COMMAND]
\`\`\`

## API Endpoints
### Create Transaction
- **Endpoint**: \`POST ...\`
- **Authentication**: [Bearer/Basic]
- **Required Parameters**:
  - \`field\` (type)
- **Optional/Pre-fill Parameters**:
  - \`field\`

### Check Status
- **Endpoint**: \`GET ...\`
- **Statuses**: [pending, paid, etc]

### Webhook Callback
- **Format**: POST
- **Authentication**: [Signature Header]
- **Secret Location**: [Dashboard/Settings]

## Verification Part
### Successful Transaction (Happy Path)
\`\`\`bash
[CURL COMMAND defined in Step 3]
\`\`\`
**Response**:
\`\`\`json
[REAL JSON RESPONSE]
\`\`\`

### Negative Testing (Validation)
| Test Case | Variation | Expected | Actual Code | JSON Error |
|-----------|-----------|----------|-------------|------------|
| Missing Name | Omit Name | 400 | 422 | \`{"error":...}\` |
| Bad Type | String Amount | 400 | 200 | (Accepted) |

## Gap Analysis (Discrepancies)
| # | Issue | Documentation | Actual Behavior | Severity |
|---|-------|---------------|-----------------|----------|
| 1 | Amount Type | Integer | String | Low |
| 2 | Email | Optional | Required (500 Error) | High |

## Questions for Provider
- [Specific technical questions]
```
