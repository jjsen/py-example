import requests
import logging
from datetime import datetime
import json
from concurrent.futures import ThreadPoolExecutor

# Configure logging
timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
logging.basicConfig(filename=f'logfile-{timestamp}.log', level=logging.INFO)

# Credentials and URLs
source_jira_url = "https://source-jira.example.com"
target_jira_url = "https://target-jira.example.com"
headers = {"Authorization": "Basic ..."}  # Authentication headers

def fetch_total_issues(jira_url):
    url = f"{jira_url}/rest/api/3/search"
    params = {
        "maxResults": 1
    }
    response = requests.get(url, headers=headers, params=params)
    total_issues = response.json()['total']
    return total_issues

def fetch_keys(jira_url, start_at=0):
    url = f"{jira_url}/rest/api/3/search"
    params = {
        "startAt": start_at,
        "maxResults": 50,
        "fields": "key"
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f'Failed to retrieve data from {jira_url}: {e}')
        return []
    else:
        issues_data = response.json()["issues"]
        keys = [issue['key'] for issue in issues_data]
        return keys

def get_remote_links(jira_url, key):
    url = f"{jira_url}/rest/api/3/issue/{key}/remotelink"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f'Failed to retrieve data from {jira_url} for {key}: {e}')
        return []
    else:
        return response.json()

def compare_and_migrate_links(key):
    source_links = get_remote_links(source_jira_url, key)
    target_links = get_remote_links(target_jira_url, key)
    
    source_urls = [link['object']['url'] for link in source_links]
    target_urls = [link['object']['url'] for link in target_links]

    for url in source_urls:
        if url not in target_urls:
            link_block = next((link for link in source_links if link['object']['url'] == url), None)
            if link_block:
                print(f'Would migrate link for {key} from {source_jira_url} to {target_jira_url}')

def process_issue_keys(issue_keys):
    for issue_key in issue_keys:
        compare_and_migrate_links(issue_key)

def main():
    logging.basicConfig(filename=f'log_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log', level=logging.INFO)
    total_issues = fetch_total_issues(source_jira_url)
    processed_issues = 0
    start_at = 0
    with ThreadPoolExecutor() as executor:
        while True:
            issue_keys = fetch_keys(source_jira_url, start_at)
            if not issue_keys:
                break  # Exit loop when no more issue keys are found
            
            executor.submit(process_issue_keys, issue_keys)
            
            processed_issues += len(issue_keys)
            progress_percentage = (processed_issues / total_issues) * 100
            print(f'Processed {processed_issues}/{total_issues} issues ({progress_percentage:.2f}%)')
            
            start_at += len(issue_keys)  # Update start_at for next batch

if __name__ == "__main__":
    main()
