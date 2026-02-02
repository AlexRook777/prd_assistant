---
description: Phase 1 Step 6 - Fill technical specifications for all project stories
---

# Step 6: Fill Project Stories

Create comprehensive technical specifications for all integration stories using the defined Epic/User Story structure and strict Gherkin acceptance criteria.

## Working Directory
`<current_integration>/1_result/`

## Output File
`6.project_stories.md`

## Required Skill
*   [.agent/skills/epic_story_creation/SKILL.md](file:///home/worker/repos/prd_assistant/.agent/skills/epic_story_creation/SKILL.md)

## Task

1.  **Read the Skill**: Read and understand the guidelines in `.agent/skills/epic_story_creation/SKILL.md`.

2.  **Pre-computation Check (CRITICAL)**:
    *   Check if `6.project_stories.md` already exists.
    *   **IF IT EXISTS**:
        *   Read the file content.
        *   Extract **Acceptance Criteria** status (checked/unchecked boxes).
        *   **Preserve** any completed criteria in the new stories by marking the corresponding Gherkin scenarios as checked `[x]`.
    *   **IF IT DOES NOT EXIST**: Proceed normally.

3.  **Compile Stories**:
    *   Use the context from: 
    `1.epic_analysis.md`, 
    `2.docs_analysis.md`, 
    `3.test_page.md`, 
    `4.auto_test_page.md`, 
    `5.betterbro_compatibility.md`.
    *   Structure the output exactly as defined in the Skill (Epic -> Stories).
    *   **CRITICAL**: All Acceptance Criteria MUST be written in **Gherkin (Given/When/Then)** format.

## Template Example

```markdown
# Epic: [Integration Name]
**Goal**: Integrate [Provider] for [Region/Currency].

## Story 1: Authorization
### Description
As a System, I want to authenticate with the provider API.

### Technical Specifications
*   **Method**: `POST /oauth2/token`
*   **Headers**: `Authorization: Basic ...`

### Acceptance Criteria

**Scenario: Successful Token Generation**
*   **Given** Valid client credentials
*   **When** I request an access token
*   **Then** I receive a 200 OK response
*   **And** The response contains an `access_token`
*   **And** The token type is `Bearer`

**Scenario: Invalid Credentials**
*   **Given** Invalid client_id or secret
*   **When** I request an access token
*   **Then** I receive a 401 Unauthorized response
```

## Success Criteria
*   Output file follows the Epic/Story/Gherkin structure.
*   All technical details (endpoints, params, mappings) are included.
*   Existing progress (if re-running) is preserved.

## User Confirmation
*   "Project Stories filled. Review `6.project_stories.md`. Should I proceed to Step 7 (Field Testing), or do you want to refine this step?"




