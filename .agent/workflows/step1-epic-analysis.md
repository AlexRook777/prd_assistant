---
description: Phase 1 Step 1 - Analyze Epic/Jira requirements
---

# Step 1: Epic Analysis

Analyze the Epic or Jira requirements to understand the integration scope and identify unclear points.

## Working Directory
`<current_integration>/1_research/`

## Output File
`1.epic_analysis.md`

## Task

1. **Read Source Documents**: 
   - Check `0_initial_docs/` for Epic description, Jira ticket, or business requirements
   - Read any PDFs, Word docs, or text files containing requirements

2. **Extract Key Information**:
   - Payment method (wallet, card, bank transfer, etc.)
   - Target countries/regions
   - Flow type (H2H, Redirect, HPP)
   - Transaction types (Payin, Payout, Refund)
   - Special requirements or constraints

3. **Identify Gaps**:
   - List any unclear or missing information
   - Formulate questions for the Product Owner
   - Flag any requirements that conflict with BetterBro standards

4. **Create Documentation**:
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

## BetterBro Compatibility
- [Any requirements that might conflict with BetterBro standards]
- [Suggested resolutions]

## Next Steps
- [ ] Clarify unclear points with PO
- [ ] Proceed to Documentation Analysis (Step 2)
```

## Success Criteria
- File `1.epic_analysis.md` created in `1_research/` folder
- All template sections filled with accurate information
- Clear list of questions if any requirements are unclear
- Summary is concise (1-2 paragraphs max)

## User Confirmation
After creating the file, ask the user:
- "Epic Analysis complete. Review `1.epic_analysis.md`. Should I proceed to Step 2 (Documentation Analysis), or do you want to refine this step?"

## 5. Logging
Run the `work_logger` skill to record the results of this step.
- **skill**: `work_logger`
- **args**:
    - `integration`: Name of the current integration
    - `step`: "Step 1: Epic Analysis"
    - `status`: "Success"
    - `output_file`: `1_research/1.epic_analysis.md`
    - `summary`: "Analyzed epic for [Provider]..."
    - `execution_details`: JSON string with:
        - `files_analyzed`: ["0_initial_docs/..."]
        - `files_edited`: ["1_research/1.epic_analysis.md"]
        - `actions`: ["Read requirements", "Identified gaps"]
        - `reasoning`: "Detailed narrative of what you did and why, including thoughts on unclear points."