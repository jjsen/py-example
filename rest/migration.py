import requests
import json
import base64

# Define your credentials and URLs
source_jira_url = ""
target_jira_url = ""
username = ""
api_token = ""

# Setup headers for requests
auth_str = f"{username}:{api_token}"
auth_encoded = base64.b64encode(auth_str.encode()).decode()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {auth_encoded}"
}

def fetch_keys(jira_url, filename):
    start_at = 0
    max_results = 50  # Maximum allowed by API
    total_fetched = 0
    total_available = None  # We'll know the total after the first request

    with open(filename, 'w') as file:
        while total_available is None or total_fetched < total_available:
            params = {
                "startAt": start_at,
                "maxResults": max_results,
                "fields": "key"  # Request only the key field for efficiency
            }
            url = f"{jira_url}/rest/api/3/search"
            response = requests.get(url, headers=headers, params=params)
            if response.status_code != 200:
                print(f'Failed to retrieve data from {jira_url}: {response.text}')
                return

            issues_data = response.json()["issues"]
            for issue in issues_data:
                file.write(f"{issue['key']}\n")

            # Update pagination variables
            if total_available is None:
                total_available = response.json()["total"]
            total_fetched += len(issues_data)
            start_at += max_results

# Fetch keys and write to files
fetch_keys(source_jira_url, 'source_keys.txt')
fetch_keys(target_jira_url, 'target_keys.txt')

# Execute the function to compare issue keys
compare_issue_keys()
