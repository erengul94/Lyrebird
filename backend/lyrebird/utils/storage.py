from google.cloud import storage

import os, requests
from datetime import timedelta


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/erengul/Documents/projects/Lyrebird/backend/lyrebird/google_service_account.json'

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


def generate_signed_url(bucket_name, blob_name, expiration_minutes=15):
    """Generate a signed URL to access a private file in GCS."""
    storage_client = storage.Client()

    # Get the bucket and blob (file) reference
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    # Generate a signed URL that expires in `expiration_minutes`
    signed_url = blob.generate_signed_url(expiration=timedelta(minutes=expiration_minutes), method="GET")

    return signed_url

def download_audio_from_url(signed_url):
    """Download the audio file from a signed URL."""
    response = requests.get(signed_url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download audio: {response.status_code}")