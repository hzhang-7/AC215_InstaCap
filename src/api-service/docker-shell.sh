#!/bin/bash

# exit immediately if a command exits with a non-zero status
set -e

# Define some environment variables
export IMAGE_NAME="mushroom-app-api-service"
export BASE_DIR=$(pwd)
export SECRETS_DIR=$(pwd)/../secrets/
export SERVICE_ACCOUNT_FILE="../secrets/model_deployment.json"
export PERSISTENT_DIR=$(pwd)/../../../persistent-folder/

# Build the image based on the Dockerfile
docker build -t $IMAGE_NAME -f Dockerfile .

# Run the container
docker run --rm --name $IMAGE_NAME -ti \
-e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
-e SERVICE_ACCOUNT_FILE=$SERVICE_ACCOUNT_FILE \
-e GCP_PROJECT=$GCP_PROJECT \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v "$PERSISTENT_DIR":/persistent \
-p 9000:9000 \
$IMAGE_NAME