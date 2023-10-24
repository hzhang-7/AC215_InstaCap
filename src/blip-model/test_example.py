# Install required libraries
# pip install requests
# pip install google-auth
import requests
import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account

import os
from PIL import Image
from io import BytesIO
import base64


if __name__ == '__main__':
    # Define the required SCOPES
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

    # service account JSON file name
    SERVICE_ACCOUNT_FILE = '../secrets/model_deployment.json'

    # Load credentials from the service account file with the specified SCOPES
    cred = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    # Create an authentication request
    auth_req = google.auth.transport.requests.Request()

    # Refresh the credentials
    cred.refresh(auth_req)

    # Obtain the bearer token
    bearer_token = cred.token

    # GCP project ID
    project_id = "ac215-project-398320"

    # Endpoint ID from the model dashboard
    endpoint_id = "6255308567394385920"

    # Define the base URL for your specific region (us-central1 in this example)
    base_url = f"https://us-central1-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/us-central1/endpoints/{endpoint_id}:predict"


    image = Image.open(os.path.join("data", "harvard.gac_2895501412861369086.jpeg"))
    buffer = BytesIO()
    image.save(buffer, format="JPEG")
    b64str = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Define the request body for your specific prompt and parameters
    request_body = {
        "instances": [
            {
                "img_str": b64str,
            }
        ]
    }

    # Define the headers with the bearer token and content type
    headers = {
        "Authorization": "Bearer {bearer_token}".format(bearer_token=bearer_token),
        "Content-Type": "application/json"
    }

    # Send a POST request to the model endpoint
    resp = requests.post(base_url, json=request_body, headers=headers)

    # Print the response from the model
    print(resp.json())