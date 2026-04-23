from google.cloud import storage
import os

BUCKET_NAME = "bucket-name"

client = storage.Client()

def upload_to_gcs(file_path, object_name):
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(object_name)

    blob.upload_from_filename(file_path)

    return blob.public_url