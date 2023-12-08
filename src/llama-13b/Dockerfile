FROM pytorch/pytorch:2.1.0-cuda11.8-cudnn8-runtime

# Set the working directory
WORKDIR /app

# Set the environment variable
ENV HF_TOKEN="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"

# Copy only the dependencies file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app.py ./

# Start the application
CMD ["python", "app.py"]