from google.cloud import storage

SYS_INPUT_BUCKET_NAME = "label-studio-images"

def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)

    for blob in blobs:
        print(blob.name)

list_blobs(SYS_INPUT_BUCKET_NAME)


# Create a .CSV file that contains the URIs to your images in your GCS bucket
import re

SYS_FILE_EXTENSIONS = ['PNG']

def check_extension(filename, extensions):
    pattern = r".*\.({})$".format('|'.join(extensions))
    return bool(re.match(pattern, filename, re.IGNORECASE))



def list_blobs(bucket_name):
    """Returns a list of URIs of the blobs in the bucket."""
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)

    uris = []
    for blob in blobs:
        if(check_extension(blob.name, SYS_FILE_EXTENSIONS)):
            uris.append("gs://{}/{}".format(bucket_name, blob.name))

    return uris

# TO DO : Change to jsonl format : {'imageGcsUri' : 'gs://label-studio-images/la_003_40.png'}

uris = list_blobs(SYS_INPUT_BUCKET_NAME)

# Upload this .CSV file to the same bucket that contains your image files
import csv
import os

# Update this to the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "ai-dl-297116-4511c50b83f1.json"

def write_uris_to_csv(uris, csv_filename):
    """Writes a list of URIs to a .CSV file."""
    with open(csv_filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Image_URI"])
        for uri in uris:
            writer.writerow([uri])

csv_filename  = "uris.csv"
csv_blob_name = "uris.csv"
write_uris_to_csv(uris, csv_filename)

from labeling_utils import upload_blob

upload_blob(SYS_INPUT_BUCKET_NAME, csv_filename, csv_blob_name)