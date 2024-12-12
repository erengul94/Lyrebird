import os
import logging
from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set your credentials for the GCS Client
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/erengul/Documents/projects/Lyrebird/backend/lyrebird/google_service_account.json'


def upload_to_gcs(bucket_name, source_file, destination_blob_name):
    """
    Uploads a file to the specified GCS bucket.

    Args:
        bucket_name (str): The name of the GCS bucket.
        source_file (File or str): The file object or file path.
        destination_blob_name (str): The path in the bucket where the file will be saved.

    Returns:
        str: The public URL of the uploaded file.
    """
    try:
        # Initialize the GCS client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Upload the file
        if hasattr(source_file, 'read'):  # If the source is a file object
            logger.info(f"Uploading file object to GCS bucket: {bucket_name}")
            blob.upload_from_file(source_file)
        elif isinstance(source_file, str):  # If the source is a file path
            logger.info(f"Uploading file from path '{source_file}' to GCS bucket: {bucket_name}")
            blob.upload_from_filename(source_file)
        else:
            logger.error(f"Invalid file type provided: {type(source_file)}")
            raise ValueError("Source file must be a file object or a file path.")

        # Optionally make the blob publicly accessible
        # blob.make_public()

        # Return the public URL of the uploaded file (if accessible)
        return blob.public_url

    except DefaultCredentialsError as e:
        logger.error(f"Google Cloud credentials error: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to upload file to GCS: {e}")
        raise


def download_file_from_gcs(bucket_name, destination_file_name, destination_blob_name):
    """
    Downloads a file from the specified GCS bucket.

    Args:
        bucket_name (str): The name of the GCS bucket.
        destination_file_name (str): The local file path where the file will be saved.
        destination_blob_name (str): The blob (file) name in GCS.

    Returns:
        google.cloud.storage.blob.Blob: The blob object.
    """
    try:
        # Initialize the GCS client
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Download the file
        logger.info(f"Downloading file from GCS bucket: {bucket_name}, blob: {destination_blob_name}")
        blob.download_to_filename(destination_file_name)

        # Return the blob object for further handling if needed
        return blob

    except DefaultCredentialsError as e:
        logger.error(f"Google Cloud credentials error: {e}")
        raise
    except Exception as e:
        logger.error(f"Failed to download file from GCS: {e}")
        raise
