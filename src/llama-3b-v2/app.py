import logging
import os
import shlex 
from flask import Flask, jsonify, request
from transformers import LlamaForCausalLM, LlamaTokenizer
import torch
import subprocess


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


## v2 models
model_path = 'openlm-research/open_llama_3b_v2'

tokenizer = LlamaTokenizer.from_pretrained(model_path)
model = LlamaForCausalLM.from_pretrained(
    model_path, torch_dtype=torch.float16, device_map='auto',
)

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
            logger.error("Invalid input_text")
            return jsonify(error="Invalid input_text"), 400

        instance = instances[0]  # Get the single instance

        input_text = instance.get("prompt")
        if not input_text or not isinstance(input_text, str):
            logger.error("Invalid input_text in the instance")
            return jsonify(error="Invalid input_text in the instance"), 400

        input_ids = tokenizer.encode(input_text, return_tensors="pt")
        output = model.generate(input_ids, max_length=100, num_beams=5, temperature=1.5)
        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

        # Return the generated text
        return jsonify(predictions=[generated_text]), 200
    

    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"Error: {str(e)}")
        # Provide a response to the user
        return jsonify(error=f"Internal server error: {str(e)}"), 500

@app.route("/v1/endpoints/<endpoint_id>/deployedModels/<deployed_model_id>", methods=["GET"])
def get_model_info(endpoint_id, deployed_model_id):
    try:
        # Use endpoint_id and deployed_model_id to
        # manage and fetch specific model info
        # Example: Fetch and return some information about the model
        model_info = {
            "model_name": "llama2-3b",
            "endpoint_id": endpoint_id,
            "deployed_model_id": deployed_model_id,
        }
        return jsonify(model_info), 200

    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"Error: {str(e)}")
        # Provide a response to the user
        return jsonify(error=f"Internal server error: {str(e)}"), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)