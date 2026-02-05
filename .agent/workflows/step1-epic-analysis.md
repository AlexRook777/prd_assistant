---
description: Phase 1 Step 1 - Analyze Epic/Jira requirements
---

# Step 1: Epic Analysis

Analyze the Epic or Jira requirements to understand the integration scope and identify unclear points.

## Working Directory
`<current_integration>/1_result/`

## Output File
`1.epic_analysis.md`

## Task

1. **Jira Content Verification (MANDATORY)**:
   - **Goal**: Ensure the `bizdev_request` file contains 100% of the information from the Jira issue before analysis begins.
   - **Locate File**: Find `0_initial_docs_and_config/bizdev_request_<IssueKey>.md`.
   - **Extract Key**: Get the Jira Issue Key from the filename.
   - **Fetch Live Data**: Run `python3 app/jira_fetcher.py <IssueKey>` to get the full, non-truncated JSON.
   - **Verification**:
     - Read the current `bizdev_request` file.
     - Compare it against the fetched JSON.
     - **Check for missing**:
       - Full description text (especially tables).
       - Transaction limits (min/max amounts, daily/monthly limits).
       - Tables in description.
       - All comments (especially recent ones).
   - **Action**:
     - **IF MISSING INFO FOUND**: Update `bizdev_request_<IssueKey>.md` immediately to include the missing data. You can use the `Jira Requirement Extraction` skill logic or manually update it.
     - **IF COMPLETE**: Proceed to next step.

2. **Pre-computation Check (CRITICAL)**:
   - Check if `1.epic_analysis.md` already exists.
   - **IF IT EXISTS**:
     - Read the **ENTIRE** file content.
     - Treat this file as the **Primary Source of Truth**. The information here (especially in "Summary", "Requirements", and "Clarified Points") supersedes the raw initial docs.
     - **Extract & Preserve**:
       - Any section labeled "Clarified Points" or "User Feedback".
       - Any Q&A pairs from "Unclear Points".
     - **Integrate**: Ensure any facts from the existing file represent the baseline for the new generation. Do not revert specific details provided by the user back to the raw docs.
     - **Augment**: Add the `## Clarified Points (User Feedback)` section if it doesn't exist, populating it with any answered questions.
   - **IF IT DOES NOT EXIST**: Proceed normally to read source documents.

3. **Read Source Documents**: 
   - Check `0_initial_docs_and_config/` for Epic description, Jira ticket, or business requirements
   - Read any PDFs, Word docs, or text files containing requirements

4. **Extract Key Information**:
   - Payment method (wallet, card, bank transfer, etc.)
   - Target countries/regions
   - Flow type (H2H, Redirect, HPP)
   - Transaction types (Payin, Payout, Refund)
   - **BetterBro Alignment**: Search for "BetterBro Service URL" or specific "Service Rule" mentioned in the ticket.
   - Special requirements or constraints

5. **Identify Gaps**:
   - List any unclear or missing information
   - Formulate questions for the Product Owner
   - Flag any requirements that conflict with BetterBro standards

6. **Create Documentation**:
   Generate `1.epic_analysis.md` using this template:

```markdown
# Epic Analysis

**Integration Name**: [Provider Name - Country - Currency - Method]  
**Date**: [Current Date]

## Summary
- **Payment Method**: [wallet/card/bank transfer/etc.]
- **Countries**: [List of countries]
- **Currencies**: [List of currencies]
- **Flow Type**: [H2H/Redirect/HPP]
- **Transaction Types**: [Payin/Payout/Refund]

## BetterBro Alignment (Draft)
- **Service Rule**: [e.g. Acquiring Form / H2H / Payouts] (if provided in Epic)
- **BetterBro Service URL**: [Link if provided] (if provided in Epic)

## Requirements
- [Bullet list of business requirements]
- [Include volume expectations if mentioned]
- [Include SLA/response time requirements]

## Technical Constraints
- [Any mentioned technical limitations]
- [Integration timeline]
- [Testing environment availability]

## Unclear Points
- [Question 1 for Product Owner]
- [Question 2 for Product Owner]
- [etc.]


## Next Steps
- [ ] Clarify unclear points with PO
- [ ] Proceed to Documentation Analysis (Step 2)
```

7. **Include Workflow Suggestions**: End the file with `## Workflow Suggestions` section (see `.gemini.md` for format).

## Success Criteria
- File `1.epic_analysis.md` created in `1_result/` folder
- All template sections filled with accurate information
- Clear list of questions if any requirements are unclear
- Summary is concise (1-2 paragraphs max)

## User Confirmation
After creating the file, ask the user:
- "Epic Analysis complete. Review `1.epic_analysis.md`. Should I proceed to Step 2 (Documentation Analysis), or do you want to refine this step?"