---
name: work_logger
description: Log the results of an agent's work step for future analysis.
---

# Work Logger Skill

Use this skill to log the outcome of a workflow step. This is crucial for the "Continuous Improvement" loop.

## Usage

When you finish a major step in a workflow (e.g., Step 1, Step 2), run the helper script to append a log entry.
You MUST provide a JSON string for `execution_details` that captures the context of your work.

### Command

```bash
python3 .agent/skills/work_logger/scripts/log_work.py \
  --integration "Integration_Name" \
  --step "Step Name" \
  --status "Success" \
  --summary "Short summary of the user request" \
  --execution_details '{"files_analyzed": ["file1", "file2"], "files_edited": ["file3"], "actions": ["Analyzed X", "Created Y"], "reasoning": "I read X to understand Y..."}'
```

### Arguments
- `--integration`: Name of the integration.
- `--step`: Name of the step (e.g., "Step 1: Epic Analysis").
- `--status`: "Success", "Failure", "Refinement".
- `--summary`: One-sentence summary.
- `--execution_details`: **JSON String** with:
    - `files_analyzed`: List of absolute paths read.
    - `files_edited`: List of absolute paths modified/created.
    - `actions`: List of high-level actions.
    - `reasoning`: Detailed narrative of your thought process (what you did and why).

### Optional Arguments
- `--output_file`: Path to the main file created in this step.
- `--issues`: Description of issues encountered.
- `--improvement`: Ideas for improvement.

## Log Location
Logs are stored in: `.agent/work_logs/work_log.jsonl`
