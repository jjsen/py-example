import requests
import json

# Define the endpoint and credentials
auth = ('username', 'api_token')

def get_ticket_count(project_key):
    url = f"https://software-dev.atlassian.net/rest/api/3/search"
    params = {
        'jql': f'project = {project_key}',
    }
    response = requests.get(url, auth=auth, params=params)
    if response.status_code != 200:
        print(f'Failed to retrieve data for project {project_key}: {response.text}')
        return 0
    data = response.json()
    return data['total']

def list_projects():
    url = "https://software-dev.atlassian.net/rest/api/3/project"
    response = requests.get(url, auth=auth)
    if response.status_code != 200:
        print(f'Failed to retrieve projects: {response.text}')
        return []
    return response.json()

def main():
    projects = list_projects()
    total_tickets = 0
    for project in projects:
        project_key = project['key']
        ticket_count = get_ticket_count(project_key)
        print(f'Project {project_key} has {ticket_count} tickets.')
        total_tickets += ticket_count
    print(f'Total number of tickets across all projects: {total_tickets}')

if __name__ == "__main__":
    main()
