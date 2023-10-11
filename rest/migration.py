import json
import requests
from concurrent.futures import ThreadPoolExecutor

# Assume keys are loaded from the text files generated in the previous step
source_keys = [line.strip() for line in open('source_keys.txt')]

# Setup headers for requests (assuming headers variable is already initialized)
headers = {
    # ... (your headers here)
}

def get_remote_links(jira_url, key):
    url = f"{jira_url}/rest/api/3/issue/{key}/remotelink"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f'Failed to retrieve data from {jira_url} for {key}: {response.text}')
        return None
    return response.json()

def compare_links(key):
    source_links = get_remote_links(source_jira_url, key)
    target_links = get_remote_links(target_jira_url, key)
    
    if source_links is None or target_links is None:
        return []

    missing_data_batch = []
    source_urls = {link['object']['url'] for link in source_links}
    target_urls = {link['object']['url'] for link in target_links}
    missing_urls = source_urls - target_urls
    
    for missing_url in missing_urls:
        missing_data_batch.append(next(link for link in source_links if link['object']['url'] == missing_url))

    return missing_data_batch

# URLs
source_jira_url = "https://software-dev.atlassian.net"
target_jira_url = "https://software.atlassian.net"

batch_size = 1000
for i in range(0, len(source_keys), batch_size):
    batch_keys = source_keys[i:i + batch_size]
    missing_data = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(compare_links, batch_keys)
    for result in results:
        missing_data.extend(result)
    # Save missing data to a file for the current batch
    with open(f'missing_data_batch_{i // batch_size + 1}.json', 'w') as file:
        json.dump(missing_data, file, indent=4)

