import requests
import json
import base64

# Define your credentials and URLs
source_jira_url = ""
username = ""
api_token = ""

# Setup headers for requests
auth_str = f"{username}:{api_token}"
auth_encoded = base64.b64encode(auth_str.encode()).decode()
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Basic {auth_encoded}"
}

def get_ticket_count():
    url = f"{source_jira_url}/rest/api/3/search"
    params = {
        "jql": "",  # Adjust the JQL query as needed
        "maxResults": 0,  # Set to 0 to only retrieve metadata
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        print(f'Failed to retrieve data: {response.text}')
        return

    total_tickets = response.json()['total']
    print(f'Total number of tickets: {total_tickets}')

# Execute the function to get the ticket count
get_ticket_count()
