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
    url = f"{jira_url}/rest/api/3/search"
    params = {
        "jql": "",  # Adjust the JQL query as needed
        "maxResults": 50,  # Adjust as needed
        "fields": "key"  # Only fetch the 'key' field
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f'Failed to retrieve issue keys from {jira_url}: {response.text}')
        return None

    issues_data = response.json()["issues"]
    issue_keys = [issue["key"] for issue in issues_data]
    return issue_keys

def compare_issue_keys():
    source_issue_keys = fetch_issue_keys(source_jira_url)
    target_issue_keys = fetch_issue_keys(target_jira_url)

    if source_issue_keys is None or target_issue_keys is None:
        return

    missing_keys = set(source_issue_keys) - set(target_issue_keys)

    print(f'Issue keys in source but not in target: {missing_keys}')
    print(f'Count of issue keys in source but not in target: {len(missing_keys)}')

# Execute the function to compare issue keys
compare_issue_keys()
