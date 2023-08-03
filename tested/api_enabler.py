from googleapiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client.client import GoogleCredentials
from google.oauth2 import service_account

# Replace with your project ID and the API you want to enable
project_id = 'monitoring'
api_to_enable = 'monitoring.googleapis.com'

# Uncomment to use Application Default Credentials (ADC)
# credentials = GoogleCredentials.get_application_default()

# Uncomment to use Service Account Credentials in Json format
credentials = service_account.Credentials.from_service_account_file('.json')

# Build the Service Usage API client
service_usage_service = discovery.build('serviceusage', 'v1', credentials=credentials)

def enable_api(project_id, api):
    try:
        request = service_usage_service.services().enable(name=f'projects/{project_id}/services/{api}')
        response = request.execute()
        print(f'Enabled {api} API for project "{project_id}".')
    except HttpError as error:
        print(f'An error occurred while enabling the API for project "{project_id}": {error}')

enable_api(project_id, api_to_enable)
