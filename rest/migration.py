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

def get_ticket_count(jira_url):
    url = f"{jira_url}/rest/api/3/search"
    params = {
        "jql": "",  
        "maxResults": 0, 
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f'Failed to retrieve data from {jira_url}: {response.text}')
        return

    total_tickets = response.json()['total']
    print(f'Total number of tickets in {jira_url}: {total_tickets}')

# Execute the function to get the ticket count for both source and target URLs
get_ticket_count(source_jira_url)
get_ticket_count(target_jira_url)
