import requests
import json
import os
from requests.auth import HTTPBasicAuth

url = "https://4billio.atlassian.net/rest/api/3/issue/IN-1137"
email = "o.hrachov@4bill.io"
token = "ATATT3xFfGF049yHCWcljDxYrbSj5R3AMO6FGOWoVlosOg8wuPFPpazwAVWmu1CQYYFq3T4HVyxzqV9lr9rIthFDbR9ZIje5Ad3cbqx_KszOyrNUo2g69OUkdRZReMe8Jj-akQehWD4Tvnufwv5oAl6kDVGdLvywG6CKKoos-MR1w3onGXNiBlU=3975C370"

auth = HTTPBasicAuth(email, token)
headers = {
   "Accept": "application/json"
}
params = {
    "expand": "renderedFields",
    "fields": "description,comment"
}

response = requests.get(url, headers=headers, params=params, auth=auth)

if response.status_code == 200:
    data = response.json()
    
    # Save raw JSON to debug if needed, but primarily write formatted content
    with open("jira_issue_full.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        
    print("Successfully fetched Jira issue data. Saved to jira_issue_full.json")
else:
    print(f"Failed to fetch issue: {response.status_code} - {response.text}")
