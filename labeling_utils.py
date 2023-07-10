def upload_blob(bucket_name, source_file_name, destination_blob_name):
    
    from google.cloud import storage

    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def download_blob(bucket_name, source_blob_name, destination_file_path):

    from google.cloud import storage
    import os

    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    
    blob.download_to_filename(destination_file_path)

    print(f"Blob {source_blob_name} downloaded to {destination_file_path}.")
