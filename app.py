import logging
from flask import Flask, jsonify, request
from transformers import AutoModelForCausalLM, AutoTokenizer
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

# Define the path to the hf-token file
token_file_path = "./src/secrets/hf-token"

# Build the command to log in using huggingface-cli
command = f"huggingface-cli login --token $(cat {token_file_path})"

# Run the command using subprocess
try:
    subprocess.run(command, shell=True, check=True)
except subprocess.CalledProcessError as e:
    print(f"Login failed: {e}")

model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-2-7b-chat-hf")
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

@app.route("/generate_text", methods=["POST"])
def generate_text():
    try:
        data = request.get_json()
        if "prompt" not in data:
            return jsonify(error="Invalid input: 'prompt' field is required."), 400

        prompt = data["prompt"]
        input_ids = tokenizer.encode(prompt, return_tensors="pt")
        output = model.generate(input_ids, max_length=100, num_return_sequences=1, do_sample=True)

        generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
        return jsonify(generated_text=generated_text), 200

    except Exception as e:
        # Log the error for debugging purposes
        logger.error(f"Error: {str(e)}")
        # Provide a response to the user
        return jsonify(error=f"Internal server error: {str(e)}"), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
 