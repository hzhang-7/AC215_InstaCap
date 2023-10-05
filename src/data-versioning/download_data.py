"""
Module that contains the command line app.
"""
import argparse
import os
import traceback
import time
from google.cloud import storage
import shutil
import glob
import json


GCS_BUCKET_NAME = os.environ["GCS_BUCKET_NAME"]
CAPTION_DIR = "captions"       # Default directory for storing captions
POST_DIR = "posts"             # Default directory for storing posts


def main(args):

    dataset_dir = args.dirpath

    print(f"Downloading data to directory {dataset_dir}")

    bucket_name = GCS_BUCKET_NAME

    # Clear dataset folders
    print(f"Clearing previous versions of data, if any...")
    shutil.rmtree(dataset_dir, ignore_errors=True, onerror=None)
    os.makedirs(dataset_dir, exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, CAPTION_DIR), exist_ok=True)
    os.makedirs(os.path.join(dataset_dir, POST_DIR), exist_ok=True)


    # Initiate Storage client
    print(f"Initializing Storage Client...")
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blobs = bucket.list_blobs()

    # Download data
    for blob in blobs:
        if not blob.name.endswith("/"):
            if blob.name.startswith(CAPTION_DIR) or blob.name.startswith(POST_DIR):
                local_filepath = os.path.join(dataset_dir, blob.name)
                blob.download_to_filename(local_filepath)
                if args.verbose:
                    print(f"Download from cloud: \t{blob.name}" + 
                        f"\n\t to local storage: \t{local_filepath}")
    print("Finish downloading all data files")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Data Versioning Script")

    parser.add_argument(
        "-d",
        "--dirpath",
        default='./data',
        type=str,
        help="Directory path for storing downloaded data",
    )
    
    parser.add_argument(
        "-v",
        "--verbose",
        action='store_true',
        help="Print out download process"
    )

    args = parser.parse_args()

    main(args)
