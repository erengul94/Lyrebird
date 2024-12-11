from google.cloud import storage

import os, requests
from datetime import timedelta


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/erengul/Documents/projects/Lyrebird/backend/consumers/google_service_account.json'

def upload_to_gcs(bucket_name, source_file, destination_blob_name):
    """
    Uploads a file to the specified GCS bucket.

    Args:
        bucket_name (str): The name of the GCS bucket.
        source_file (File): The file object or file path.
        destination_blob_name (str): The path in the bucket where the file will be saved.

    Returns:
        str: The public URL of the uploaded file.
    """
    # Initialize the GCS client

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the file
    if hasattr(source_file, 'read'):  # For file objects (e.g., from Django forms)
        blob.upload_from_file(source_file)
    else:  # For file paths
        blob.upload_from_filename(source_file)

    # Make the blob publicly accessible (optional)
    # blob.make_public()

    return blob.public_url

