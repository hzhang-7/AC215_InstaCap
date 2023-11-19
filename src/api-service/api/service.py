from fastapi import FastAPI, File, UploadFile, Form
from starlette.middleware.cors import CORSMiddleware

import argparse
import base64
from io import BytesIO
from PIL import Image
import re
import os
import requests
import google.auth
import google.auth.transport.requests
from google.oauth2 import service_account

def process_image(image_file):
    '''
    processing an image based on a given file path
    '''
    try:
        image = Image.open(image_file.file)
        buffer = BytesIO()
        image.save(buffer, format="JPEG")
        b64str = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return b64str
    except Exception as e:
        print(f'Error processing image: {e}')
        return None
    
def prompt_blip(processed_image, bearer_token, blip_base_url):
    '''
    sending image to BLIP to get image transcription

    returns the blip transcription of a given image (string)
    '''
    # Define the request body for your specific prompt and parameters
    request_body = {
        "instances": [
            {
                "img_str": processed_image,
            }
        ]
    }

    # Define the headers with the bearer token and content type
    headers = {
        "Authorization": "Bearer {bearer_token}".format(bearer_token=bearer_token),
        "Content-Type": "application/json"
    }

    # Send a POST request to the model endpoint
    resp = requests.post(blip_base_url, json=request_body, headers=headers)
    response = resp.json()
    print(response)
    return response['predictions'][0][0]

def prompt_llama(prompt, bearer_token, llama_base_url):
    '''
    passing in prompt to deployed llama
    '''
    # Defining the request body for our specific prompt and parameters
    request_body = {
        "instances": [
            {
                "prompt": prompt,
            }
        ]
    }

    # Define the headers with the bearer token and content type
    headers = {
        "Authorization": "Bearer {bearer_token}".format(bearer_token=bearer_token),
        "Content-Type": "application/json"
    }
    # Send a POST request to the model endpoint
    resp = requests.post(llama_base_url, json=request_body, headers=headers)
    response = resp.json()
    print(resp.json())
    return response['predictions']



# Setup FastAPI app
app = FastAPI(title="API Server", description="API Server", version="v1")

# Enable CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
@app.get("/")
async def get_index():
    return {"message": "Welcome to the API "}

@app.post("/generate_caption/")
async def generate_caption(
    image: UploadFile = File(...),
    word: str = Form(...),
):
    tone = word
    processed_image = process_image(image)
    
    SCOPES = ['https://www.googleapis.com/auth/cloud-platform']

    # service account JSON file name
    # SERVICE_ACCOUNT_FILE = '../secrets/model_deployment.json'
    SERVICE_ACCOUNT_FILE = os.getenv("SERVICE_ACCOUNT_FILE")

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
    blip_endpoint_id = '6335353013896478720' # changes every time you deploy

    # Define the base URL for your specific region (us-central1 in this example)
    blip_base_url = f"https://us-central1-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/us-central1/endpoints/{blip_endpoint_id}:predict"

    # defining llama endpoints:
    llama_endpoint_id = '5438784844328861696'
    llama_base_url = f"https://us-central1-aiplatform.googleapis.com/v1beta1/projects/{project_id}/locations/us-central1/endpoints/{llama_endpoint_id}:predict"
    if processed_image is None:
        print(f"Error processing image")
    else:
        print("Image processed successfully! Sending to BLIP...")
        blip_transcription = prompt_blip(processed_image, bearer_token, blip_base_url)

        print(f'BLIP caption: {blip_transcription}')
        # get llama caption:
        prompt = f'Q: What is one {tone} Instagram caption of {blip_transcription}. Please give only the caption with no other text. A:'
        llama_response = prompt_llama(prompt=prompt, bearer_token=bearer_token, llama_base_url=llama_base_url)
        # try:
        #     # fixing formatting issues in raw llama response to get caption
        #     llama_answers = re.findall(r'A: "(.*?)"', llama_response[0])
        #     caption = llama_answers[0]
        # except:
        #     caption = llama_response[0]
        caption = llama_response[0].split("A: ")[1]
        print(f'Llama IG caption: {caption}')

    return {"caption": caption}