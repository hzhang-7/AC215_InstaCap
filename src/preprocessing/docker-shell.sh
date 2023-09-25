#!/bin/bash

set -e

export GCP_PROJECT="ac215-project"
export GCP_ZONE="us-central1-a"
export GOOGLE_APPLICATION_CREDENTIALS="../secrets/data_service_account.json"
export PERSISTENT_DIR=$(pwd)/../persistent-folder/
export SECRETS_DIR=$(pwd)/../secrets/

# Build the image based on the Dockerfile
docker build -t web-scraper -f Dockerfile .

# Run Container
docker run --rm -ti \
  -e GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
  -e GCP_PROJECT=$GCP_PROJECT \
  -e GCP_ZONE=$GCP_ZONE \
  --mount type=bind,source="$(pwd)",target=/app \
  --mount type=bind,source="$PERSISTENT_DIR",target=/persistent \
  --mount type=bind,source="$SECRETS_DIR",target=/secrets \
  web-scraper