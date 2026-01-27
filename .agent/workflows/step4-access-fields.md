---
description: Phase 1 Step 4 - Verify credentials and compare required fields
---

# Step 4: Access & Field Verification

Verify API credentials work and compare required fields between the system and provider documentation.

## Working Directory
`<current_integration>/1_research/`

## Output File
`4.access_and_fields.md`

## Task

1. **Verify API Access**:
   - Test credentials from `config` file
   - Confirm successful authentication
   - Document portal access (if applicable)

2. **Field Comparison**:
   - Review fields required by provider (from Step 2 analysis)
   - Compare against BetterBro's standard service fields
   - Identify missing or extra fields

3. **Create Documentation**:

```markdown
# Access & Field Verification

**Date**: [Current Date]

## Access Status

### API Credentials
- **Client ID**: ✅ Valid
- **Client Secret**: ✅ Valid
- **API Endpoint**: ✅ Reachable
- **Sandbox/Production**: [Sandbox]

### Portal Access
- **Login URL**: [URL if exists]
- **Access Status**: [Granted / Pending]
- **Portal Features**: [Dashboard, Reports, etc.]

## Field Comparison

### Required by Provider

| Field | Type | Format | Example |
|-------|------|--------|---------|
| `email` | string | Email | `user@example.com` |
| `phone` | string | E.164 | `+593991234567` |
| `document_id` | string | Alphanumeric | `1234567890` |
| `amount` | integer | Cents | `1000` |

### BetterBro Standard Fields

| Internal Field | Maps To Provider | Status | Notes |
|----------------|------------------|--------|-------|
| `customer.email` | `email` | ✅ Match | Direct mapping |
| `customer.phone` | `phone` | ⚠️ Format | Need E.164 conversion |
| `customer.document` | `document_id` | ✅ Match | |
| `transaction.amount` | `amount` | ⚠️ Transform | Multiply by 100 (cents) |

### Gap Analysis
- **Missing Fields**: [Fields provider requires but we don't collect]
- **Extra Fields**: [Fields we have but provider doesn't need]
- **Transformation Needed**: [Fields requiring format conversion]

## Issues & Resolutions
- [List any field mapping challenges]
- [Proposed solutions]

## Next Steps
- [ ] Proceed to Step 5 (Compatibility Check)
```

## Success Criteria
- Credentials verified and documented
- Field comparison table complete
- All mismatches and transformations identified

## User Confirmation
- "Access & Field verification complete. Review `4.access_and_fields.md`. Should I proceed to Step 5 (Compatibility), or do you want to refine this step?"

## 5. Logging
Run the `work_logger` skill to record the results of this step.
- **skill**: `work_logger`
- **args**:
    - `integration`: Name of the current integration
    - `step`: "Step 4: Access & Fields"
    - `status`: "Success"
    - `output_file`: `1_research/4.access_and_fields.md`
    - `summary`: "Verified credentials and field requirements..."
    - `execution_details`: JSON string with:
        - `files_analyzed`: ["1_research/2.docs_analysis.md"]
        - `files_edited`: ["1_research/4.access_and_fields.md"]
        - `actions`: ["Checked credentials", "Compared fields"]
        - `reasoning`: "Narrative of the field comparison logic and any mismatches found."

