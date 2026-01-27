import argparse
import json
import os
import datetime
from pathlib import Path

def log_work():
    parser = argparse.ArgumentParser(description='Log agent work')
    parser.add_argument('--integration', required=True, help='Name of the integration')
    parser.add_argument('--step', required=True, help='Step name (e.g., Step 1)')
    parser.add_argument('--status', required=True, help='Status: Success, Failure, etc.')
    parser.add_argument('--summary', required=True, help='High-level request summary')
    parser.add_argument('--output_file', help='Path to main output file')
    
    # New Rich Logging Arguments
    parser.add_argument('--execution_details', help='JSON string containing files_analyzed, files_edited, actions, reasoning')
    
    parser.add_argument('--issues', help='Issues encountered')
    parser.add_argument('--improvement', help='Improvement ideas')
    
    args = parser.parse_args()
    
    log_dir = Path('.agent/work_logs')
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / 'work_log.jsonl'
    
    # Parse execution details if provided
    exec_details = {}
    if args.execution_details:
        try:
            exec_details = json.loads(args.execution_details)
        except json.JSONDecodeError:
            print(f"Warning: Could not parse execution_details JSON: {args.execution_details}")
            exec_details = {"raw_error": args.execution_details}

    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "integration": args.integration,
        "workflow_step": args.step,
        "status": args.status,
        "summary": args.summary,
        "output_file": args.output_file,
        "execution_details": exec_details,
        "issues_encountered": args.issues,
        "improvement_ideas": args.improvement
    }
    
    # Filter None values (optional, but good for cleanliness)
    entry = {k: v for k, v in entry.items() if v is not None}
    
    with open(log_file, 'a') as f:
        f.write(json.dumps(entry) + '\n')
    
    print(f"Log appended to {log_file}")

if __name__ == '__main__':
    log_work()
