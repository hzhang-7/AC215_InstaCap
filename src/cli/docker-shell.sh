#!/bin/bash

set -e

export GCP_PROJECT="ac215-project"
export SECRETS_DIR=$(pwd)/../secrets/
export SERVICE_ACCOUNT_FILE="../secrets/model_deployment.json"

# Build the image based on the Dockerfile
docker build -t cli-image -f Dockerfile .

# Run Container
docker run --rm -ti \
  -e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
  -e SERVICE_ACCOUNT_FILE=$SERVICE_ACCOUNT_FILE \
  -e GCP_PROJECT=$GCP_PROJECT \
  --mount type=bind,source="$(pwd)",target=/app \
  --mount type=bind,source="$SECRETS_DIR",target=/secrets \
  cli-image

pipenv shell  # activate virtual environment inside the container