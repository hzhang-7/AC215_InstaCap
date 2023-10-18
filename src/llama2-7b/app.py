import logging
import os
import shlex 
from flask import Flask, jsonify, request
from transformers import LlamaForCausalLM, AutoTokenizer
import transformers
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

model = LlamaForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

@app.route("/v1/endpoints/<endpoint_id>/deployedModels/<deployed_model_id>", methods=["POST"])
def predict(endpoint_id, deployed_model_id):
    try:
        data = request.get_json()
        if "prompt" not in data:
            return jsonify(error="Invalid input: 'prompt' field is required."), 400

        prompt = data["prompt"]
        inputs = tokenizer(prompt, return_tensors="pt")
        output = model.generate(inputs.input_ids, max_length=100)

        generated_text = tokenizer.batch_decode(output, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
        return jsonify(generated_text=generated_text), 200

    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"Error: {str(e)}")
        # Provide a response to the user
        return jsonify(error=f"Internal server error: {str(e)}"), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
 