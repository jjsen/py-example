import requests
import json

# Credentials and URLs
source_jira_url = "https://source-jira.example.com"
target_jira_url = "https://target-jira.example.com"
headers = {"Authorization": "Basic ..."}  # Authentication headers

def fetch_keys(jira_url, start_at=0):
    url = f"{jira_url}/rest/api/3/search"
    params = {
        "startAt": start_at,
        "maxResults": 50,
        "fields": "key"
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f'Failed to retrieve data from {jira_url}: {response.text}')
        return None

    issues_data = response.json()["issues"]
    keys = [issue['key'] for issue in issues_data]
    return keys

def get_remote_links(jira_url, key):
    url = f"{jira_url}/rest/api/3/issue/{key}/remotelink"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f'Failed to retrieve data from {jira_url} for {key}: {response.text}')
        return None
    return response.json()

def compare_and_migrate_links(key):
    source_links = get_remote_links(source_jira_url, key)
    target_links = get_remote_links(target_jira_url, key)

    if source_links is None or target_links is None:
        return

    source_urls = {link['object']['url']: link for link in source_links}
    target_urls = {link['object']['url']: link for link in target_links}

    for url, link in source_urls.items():
        if url not in target_urls:
            migrate_remote_link(target_jira_url, key, link)

def migrate_remote_link(jira_url, key, link):
    migration_headers = headers.copy()
    migration_headers.update({"notifyUsers": "false"})
    url = f"{jira_url}/rest/api/3/issue/{key}/remotelink"
    response = requests.post(url, headers=migration_headers, json=link)
    if response.status_code != 201:
        print(f'Failed to migrate link for {key}: {response.text}')

def main():
    start_at = 0
    while True:
        issue_keys = fetch_keys(source_jira_url, start_at)
        if not issue_keys:
            break  # Exit loop when no more issue keys are found

        for issue_key in issue_keys:
            compare_and_migrate_links(issue_key)

        start_at += len(issue_keys)  # Update start_at for next batch

if __name__ == "__main__":
    main()





def main():
    issue_key = "YOUR_ISSUE_KEY_HERE"  # Replace with your specific issue key
    compare_and_migrate_links(issue_key)
