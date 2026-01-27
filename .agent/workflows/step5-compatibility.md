---
description: Phase 1 Step 5 - Check compatibility with system architecture
---

# Step 5: Compatibility Check

Verify the provider's integration is compatible with the current system architecture.

## Working Directory
`<current_integration>/1_research/`

## Output File
`5.compatibility.md`

## Task

1. **Architecture Review**:
   - Check if integration fits standard flow (H2H, Redirect, HPP)
   - Identify any architectural mismatches
   - Review webhook handling compatibility

2. **Create Documentation**:

```markdown
# Compatibility Check

**Date**: [Current Date]

## Flow Compatibility

### Payment Flow Type
- **Type**: [H2H / Redirect / HPP]
- **Standard Flow Compatible**: [Yes / No]
- **Rationale**: [Explanation]

### Webhook Support
- **Provider Supports Webhooks**: [Yes / No]
- **Webhook Authentication**: [Signature / IP Whitelist / None]
- **Compatible with System**: [Yes / No / Needs Custom Logic]

## Architectural Assessment

### Standard Components
| Component | Compatible | Notes |
|-----------|-----------|-------|
| Authentication | ✅ Yes | OAuth 2.0 supported |
| Transaction Creation | ✅ Yes | Standard POST endpoint |
| Status Polling | ✅ Yes | GET endpoint available |
| Webhook Handling | ⚠️ Custom | Requires HMAC validation |
| Error Handling | ✅ Yes | Standard error codes |

### Custom Logic Required
- [List any custom implementations needed]
- [Deviations from standard flow]

### Blocking Issues
- [None / List critical blockers]

### Risk Assessment
- **Low Risk**: [Standard integration, well-documented]
- **Medium Risk**: [Minor custom logic needed]
- **High Risk**: [Significant architectural changes required]

## Recommendations
- [Use standard integration template]
- [OR: Create custom middleware for X]
- [OR: Request architectural review]

## Next Steps
- [ ] Proceed to Step 6 (Fill Project Stories)
```

## Success Criteria
- Compatibility assessed across all components
- Risks identified and rated
- Clear recommendation provided

## User Confirmation
"Compatibility Check complete. Review `5.compatibility.md`. Proceed to Step 6 or refine?"

## 5. Logging
Run the `work_logger` skill to record the results of this step.
- **skill**: `work_logger`
- **args**:
    - `integration`: Name of the current integration
    - `step`: "Step 5: Compatibility"
    - `status`: "Success"
    - `output_file`: `1_research/5.compatibility.md`
    - `summary`: "Checked architectural compatibility..."
    - `execution_details`: JSON string with:
        - `files_analyzed`: ["1_research/1.epic_analysis.md", "1_research/2.docs_analysis.md"]
        - `files_edited`: ["1_research/5.compatibility.md"]
        - `actions`: ["Assessed flow", "Checked webhooks"]
        - `reasoning`: "Narrative of the compatibility assessment and any risks identified."

