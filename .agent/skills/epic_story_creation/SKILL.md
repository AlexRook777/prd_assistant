---
name: Epic and User Story Creation
description: Guide and structure for creating technical Epics and User Stories with Gherkin acceptance criteria
---

# Epic and User Story Creation Skill

This skill defines the standard approach for structuring technical requirements into Epics and User Stories, specifically tailored for integration projects. It emphasizes the use of Gherkin syntax for Acceptance Criteria (AC) to ensure clarity and testability.

## Structure

### 1. Epic
The Epic represents the high-level goal, typically the integration of a specific provider (e.g., "SmartFastPay Ecuador USD Payin").

**Format:**
```markdown
# Epic: [Integration Name]
**Goal**: [Brief description of the integration goal]
```

### 2. User Stories
User Stories break down the Epic into deliverable chunks of value. Each story must follow this structure:

**Format:**
```markdown
## Story [N]: [Title]

### Description
As a [Role], I want [Feature] so that [Benefit].

### Technical Specifications
*   **Endpoint**: [Method] [URL]
*   **Parameters**: [List or Table]
*   **Response**: [JSON Example]

### Acceptance Criteria (Gherkin)
All acceptance criteria must be written in strict Gherkin syntax (Given/When/Then).

**Scenario 1: [Name]**
*   **Given** [Precondition]
*   **When** [Action]
*   **Then** [Expected Result]

**Scenario 2: [Name]**
*   ...
```

## Standard Stories for Integrations

For payment integrations, the following stories are typically required:

1.  **Authorization**: Token management, API keys, or signature generation.
2.  **Transaction Creation (PayIn/PayOut)**: Generating the payment link or initiating transfer.
3.  **Webhook Handling**: Verifying signatures, parsing payloads, mapping statuses.
4.  **Transaction Status Check**: Manual polling implementation.
5.  **Error Handling & Validation**: Mapping provider specific error codes to internal standard errors.
6.  **Refunds (if applicable)**: Processing refunds.

## Detailed Logic

### Input
*   **Analysis Artifacts**: `1.epic_analysis.md`, `2.docs_analysis.md`, `3.test_page.md`.
*   **Context**: Provider documentation and test results.

### Output
*   **File**: `6.project_stories.md` (or specific path defined by workflow).

### Gherkin Guidelines
1.  **Atomic**: Each scenario should test one specific behavior.
2.  **Declarative**: Describe *what* happens, not *how* (implementation details belong in Tech Specs).
3.  **Measurable**: The "Then" step must be explicitly verifiable.

## Example

```markdown
## Story 2: PayIn Transaction Creation

### Description
As a Merchant, I want to create a payment link so my customer can pay.

### Technical Specifications
*   **POST** `/v2/payin`
*   **Body**: `{ "amount": 10.00, ... }`

### Acceptance Criteria

**Scenario: Successful Creation**
*   **Given** Valid customer data and amount > $6
*   **When** I send a POST request to `/v2/payin`
*   **Then** I receive a 200 OK response
*   **And** The response contains a valid `payment_url`
*   **And** The transaction status is `pending`

**Scenario: Validation Error**
*   **Given** An amount of $5 (below minimum)
*   **When** I send a POST request to `/v2/payin`
*   **Then** I receive a 400 Bad Request
*   **And** The error code is `-201`
```

```markdown
## Story 5: Error Handling & Validation

### Description
As a User, I want to receive clear error messages so that I know why my payment failed.

### Technical Specifications
*   **Map provider error codes** (e.g., `-201`) to internal error references.

### Acceptance Criteria

**Scenario: Mapping Specific Provider Error**
*   **Given** The provider returns error code `-201`
*   **When** The system processes the error response
*   **Then** The system maps it to internal error `INVALID_AMOUNT`
*   **And** The user receives the message "Amount must be between defined limits"

**Scenario: Handling Unknown Errors**
*   **Given** The provider returns an unknown error code `999`
*   **When** The system processes the error response
*   **Then** The system maps it to internal error `PROVIDER_ERROR`
*   **And** The user receives the message "An unexpected error occurred at the provider"
```
