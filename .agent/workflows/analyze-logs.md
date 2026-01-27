---
description: Analyze work logs to identify friction points and propose improvements.
---

# Analyze Work Logs

This workflow analyzes the JSONL logs in `.agent/work_logs/work_log.jsonl` to find patterns of failure, friction, or repetitive manual corrections.

## Input
- `.agent/work_logs/work_log.jsonl`

## Output
- `work_analysis_report.md` (in the current directory or a centralized location)

## Task

1. **Read the Logs**:
   - Read the content of `.agent/work_logs/work_log.jsonl`.
   - Parse the JSON entries.

2. **Analyze Patterns**:
   - Count success vs. failure rates per step.
   - Group "issues_encountered" by step.
   - Group "improvement_ideas" by step.
   - Identify which steps seem to require the most manual refinement (e.g., if a step is logged multiple times for the same integration).

3. **Generate Report**:
   Create a markdown report summarizing the findings.

   ```markdown
   # Agent Work Analysis Report
   **Date**: [Today]

   ## Summary
   - **Total Steps Executed**: [N]
   - **Success Rate**: [X]%
   - **Most Problematic Step**: [Step Name]

   ## Step Analysis

   ### [Step Name]
   - **Executions**: [N]
   - **Failures/Refinements**: [N]
   - **Common Issues**:
     - [Issue 1]
     - [Issue 2]
   - **Suggested Improvements**:
     - [Idea from logs]

   ## Action Items
   - [ ] Implement improvement X for Step Y
   ```

4. **User Notification**:
   - "Analysis complete. Review the report. Shall I implement any of the suggested improvements?"
