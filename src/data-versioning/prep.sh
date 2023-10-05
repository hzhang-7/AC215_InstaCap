#!/bin/bash

set -e

git init . --initial-branch=main
git remote add origin git@github.com:hzhang-7/AC215_InstaCap_data_versioning.git
git pull origin main