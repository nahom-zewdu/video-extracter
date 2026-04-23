# app/uploader.py

from google.cloud import storage

BUCKET_NAME = "bucket-name"

def get_client():
    return storage.Client()

def upload_to_gcs(file_path, object_name):
    client = get_client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(object_name)

    blob.upload_from_filename(file_path)

    return blob.public_url