import os
from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials
from google.oauth2 import service_account

# Uncomment to use Application Default Credentials (ADC)
# credentials = GoogleCredentials.get_application_default()

# Uncomment to use Service Account Credentials in Json format
credentials = service_account.Credentials.from_service_account_file('.json')

# Replace with the API you want to enable
api_to_enable = 'monitoring.googleapis.com'


def enable_api(project_id, api):
    service_usage_service = discovery.build('serviceusage', 'v1', credentials=credentials)
    try:
        request = service_usage_service.services().enable(name=f'projects/{project_id}/services/{api}')
        response = request.execute()
        print(f'Enabled {api} API for project "{project_id}".')
    except HttpError as error:
        error_message = str(error)
        if "not found or permission denied" in error_message:
            print(f"Project '{project_id}' not found (deleted) or permission denied. Skipping...")
        else:
            print(f'An error occurred while enabling the API for project "{project_id}": {error}')


def check_api_enabled(project_id, api):
    service_usage_service = discovery.build('serviceusage', 'v1', credentials=credentials)
    request = service_usage_service.services().list(parent=f'projects/{project_id}', filter=f'state:ENABLED')

    while request is not None:
        try:
            response = request.execute()
            services = response.get('services', [])

            for item in services:
                name = item['config']['name']
                if name == api:
                    print(f'{api} being enabled for project "{project_id}".')
                    return True

            request = service.services().list_next(previous_request=request, previous_response=response)
        except HttpError as error:
            error_message = str(error)
            if "not found or permission denied" in error_message:
                print(f"Project '{project_id}' not found (deleted) or permission denied. Skipping...")
            else:
                print(f"An error occurred: {error}")
            return False
        except Exception as e:
            print(e)
            exit(1)

    print(f'{api} is not enabled for project "{project_id}".')
    return False



# Build the Cloud Resource Manager API client
service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)
request = service.projects().list()

while request is not None:
    try:
        response = request.execute()

        for project in response.get('projects', []):
            project_id = project['projectId']
            print(f'Processing project: {project_id}')
            enable_api(project_id, api_to_enable)
            check_api_enabled(project_id, api_to_enable)

        request = service.projects().list_next(previous_request=request, previous_response=response)
    except HttpError as error:
        error_message = str(error)
        if "has been deleted" in error_message:
            print("Skipping a deleted project.")
        else:
            print(f"An error occurred: {error}")
        request = service.projects().list_next(previous_request=request, previous_response={})
