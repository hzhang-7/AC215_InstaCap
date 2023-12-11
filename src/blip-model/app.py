import logging
import os
import shlex 
from flask import Flask, jsonify, request
import torch
import subprocess

from transformers import AutoProcessor, BlipForConditionalGeneration
from PIL import Image
from io import BytesIO
import base64


logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Read the Hugging Face token from the environment variable
token_val = os.getenv("HF_TOKEN")

# Build the command to log in using huggingface-cli
command = f"huggingface-cli login --token {token_val}"

# Split the command into a list for safe execution
command_list = shlex.split(command)

# Run the command using subprocess
try:
    subprocess.run(command_list, check=True)
except subprocess.CalledProcessError as e:
    print(f"Login failed: {e}")


# Load models and processors
model_path = 'Salesforce/blip-image-captioning-base'
processor = AutoProcessor.from_pretrained(model_path)
model = BlipForConditionalGeneration.from_pretrained(model_path).to("cuda")


# Function to log SafeTensors
def log_safetensors(safetensors):
    for key, value in safetensors.items():
        logger.info(f"SafeTensor '{key}': {value}")


@app.route("/v1/endpoints/<endpoint_id>/deployedModels/<deployed_model_id>", methods=["POST"])
def predict(endpoint_id, deployed_model_id):
    try:
        # Validate and extract input_text from request JSON
        instances = request.json.get("instances")

        if not instances or not isinstance(instances, list) or len(instances) != 1:
            err_msg = "Invalid json input format"
            logger.error(err_msg)
            return jsonify(error=f"'predict': {err_msg}"), 400

        instance = instances[0]  # Get the single instance

        b64str = instance.get("img_str")
        image = Image.open(BytesIO(base64.b64decode(b64str)))

        if not image or not isinstance(image, Image.Image):
            err_msg = "Invalid image in the instance"
            logger.error(err_msg)
            return jsonify(error=f"'predict': {err_msg}"), 400

        processed_image = processor.image_processor.preprocess(image, return_tensors="pt").to("cuda")["pixel_values"]
        raw_output = model.generate(processed_image, max_length=100)
        generated_text = processor.batch_decode(raw_output, skip_special_tokens=True)

        # Return the generated text
        return jsonify(predictions=[generated_text]), 200
    
    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"Error: {str(e)}")
        # Provide a response to the user
        return jsonify(error=f"'predict' - Internal server error: {str(e)}"), 500

@app.route("/v1/endpoints/<endpoint_id>/deployedModels/<deployed_model_id>", methods=["GET"])
def get_model_info(endpoint_id, deployed_model_id):
    try:
        # [Optional] You may use endpoint_id and deployed_model_id to
        # manage and fetch specific model info
        # Example: Fetch and return some information about the model
        model_info = {
            "model_name": "pre-trained blip",
            "endpoint_id": endpoint_id,
            "deployed_model_id": deployed_model_id,
        }
        return jsonify(model_info), 200

    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"Error: {str(e)}")
        # Provide a response to the user
        return jsonify(error=f"'get_model_info' - Internal server error: {str(e)}"), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)