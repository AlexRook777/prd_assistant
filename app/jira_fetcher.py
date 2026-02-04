import requests
import json
import os
import sys
from requests.auth import HTTPBasicAuth

# Manually load .env file to avoid external dependencies
def load_env():
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def fetch_jira_issue(issue_key):
    load_env()
    email = os.getenv("ATLASSIAN_EMAIL")
    token = os.getenv("ATLASSIAN_API_TOKEN")
    domain = os.getenv("ATLASSIAN_DOMAIN")
    
    if not email or not token or not domain:
        print("Error: ATLASSIAN_EMAIL, ATLASSIAN_API_TOKEN, or ATLASSIAN_DOMAIN not found in environment.")
        sys.exit(1)

    url = f"https://{domain}/rest/api/3/issue/{issue_key}"
    auth = HTTPBasicAuth(email, token)
    headers = {
       "Accept": "application/json"
    }
    # Fetch all relevant fields including comments
    params = {
        "expand": "renderedFields",
        "fields": "summary,description,comment,created,updated,status"
    }

    try:
        response = requests.get(url, headers=headers, params=params, auth=auth)
        
        if response.status_code == 200:
            data = response.json()
            # Output plain JSON to stdout for the agent/workflow to capture
            print(json.dumps(data, indent=2))
        else:
            print(f"Error: Failed to fetch issue {issue_key}. Status: {response.status_code}")
            print(response.text)
            sys.exit(1)
            
    except Exception as e:
        print(f"Error: An exception occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 jira_fetcher.py <ISSUE_KEY>")
        sys.exit(1)
    
    issue_key = sys.argv[1]
    fetch_jira_issue(issue_key)
