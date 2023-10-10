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

def get_remote_links(jira_url, project_key):
    url = f"{jira_url}/rest/api/3/issue/{project_key}/remotelink?properties=*all"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f'Failed to retrieve data from {jira_url} for project {project_key}: {response.text}')
        return None
    return response.json()

def compare_links(project_key):
    source_links_json = get_remote_links(source_jira_url, project_key)
    target_links_json = get_remote_links(target_jira_url, project_key)

    if source_links_json is None or target_links_json is None:
        return

    source_keys = {link['key'] for link in source_links_json}
    target_keys = {link['key'] for link in target_links_json}

    missing_keys = source_keys - target_keys

    print(f'Keys in source but not in target for project {project_key}: {missing_keys}')
    print(f'Count of keys in source but not in target for project {project_key}: {len(missing_keys)}')

def fetch_project_keys():
    url = f"{source_jira_url}/rest/api/3/search"
    params = {
        "jql": "remotelinkscount>0",
        "maxResults": 50,
        "fields": "id,key"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f'Failed to retrieve project keys: {response.text}')
        return []

    issues_data = response.json()["issues"]
    for issue in issues_data:
        compare_links(issue['key'])

# Execute the function to fetch project keys and compare links
fetch_project_keys()









auth_str = f"{username}:{api_token}"
auth_encoded = base64.b64encode(auth_str.encode()).decode()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {auth_encoded}"
}

def fetch_issue_keys(jira_url):
    start_at = 0
    max_results = 100  # Set to a reasonable value to balance performance with the number of requests
    issue_keys = []

    while True:
        url = f"{jira_url}/rest/api/3/search"
        params = {
            "jql": "",  # Adjust the JQL query as needed
            "startAt": start_at,
            "maxResults": max_results,
            "fields": "key"  # Only fetch the 'key' field
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f'Failed to retrieve issue keys from {jira_url}: {response.text}')
            return None

        issues_data = response.json()["issues"]
        if not issues_data:
            break  # Exit the loop if there are no more issues to fetch

        issue_keys.extend(issue["key"] for issue in issues_data)
        start_at += max_results  # Update the startAt parameter for the next request

    return issue_keys

def compare_issue_keys():
    source_issue_keys = fetch_issue_keys(source_jira_url)
    target_issue_keys = fetch_issue_keys(target_jira_url)

    if source_issue_keys is None or target_issue_keys is None:
        return

    missing_keys = set(source_issue_keys) - set(target_issue_keys)

    # Write the results to text files
    with open('missing_keys.txt', 'w') as file:
        for key in missing_keys:
            file.write(f'{key}\n')

    with open('summary.txt', 'w') as file:
        file.write(f'Count of issue keys in source but not in target: {len(missing_keys)}\n')

# Execute the function to compare issue keys
compare_issue_keys()
