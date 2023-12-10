#!/bin/bash

set -e

export IMAGE_NAME="instacap-frontend-react"

apt-get update
apt-get install -y nodejs npm

# Install react-dropzone
npm install react-dropzone
# docker build -t $IMAGE_NAME -f Dockerfile.dev .
docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .
docker run --rm --name $IMAGE_NAME -ti -v "$(pwd)/:/app/" -p 3000:3000 $IMAGE_NAME