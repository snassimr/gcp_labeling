from google.cloud import storage

SYS_INPUT_BUCKET_NAME = "label-studio-images"
SYS_OUTPUT_BUCKET_NAME = "label-studio-images-target"

def get_blobs_list(bucket_name):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()

    blobs = storage_client.list_blobs(bucket_name)

    jsonl_blobs = []

    for blob in blobs:
        jsonl_blobs.append(blob.name)

    return jsonl_blobs

jsonl_blobs = get_blobs_list(SYS_OUTPUT_BUCKET_NAME)

# Download jsonl files
import os
import importlib
import labeling_utils
labeling_utils = importlib.reload(labeling_utils)

import re
from labeling_utils import download_blob

destination_folder = 'labeling_output'
jsonls = []
for jsonl_blob in jsonl_blobs:
    jsonl_file_name = re.sub(re.escape(os.sep), '_', jsonl_blob)
    jsonl_file_path = os.path.join(destination_folder, jsonl_file_name)
    download_blob(SYS_OUTPUT_BUCKET_NAME, jsonl_blob, jsonl_file_path)
    jsonls.append(jsonl_file_path)

# Read jsonl files
import json

labeling_data = dict()
for jsonl in jsonls:
    # Open the file in read mode ('r')
    with open(jsonl, 'r') as f:
        for line in f:
            json_dict = json.loads(line)  # Read JSON line
            i_image_uri = json_dict['imageGcsUri']
            i_labeling_data = dict()
            i_labeling_data['bb'] = json_dict['boundingBoxAnnotations']
            labeling_data[i_image_uri] = i_labeling_data


# Visualize object detection for given image
# Shared install : sudo apt-get update && sudo apt-get install -y python3-opencv
import cv2
import matplotlib.pyplot as plt

# Set image name
SYS_IMAGE_BLOB_NAME = 'la_003_40.png'
destination_folder  = 'input_images'
# Download and load image
image_file_path = os.path.join(destination_folder, SYS_IMAGE_BLOB_NAME)
download_blob(SYS_INPUT_BUCKET_NAME, SYS_IMAGE_BLOB_NAME, image_file_path)
image = cv2.imread(image_file_path)

# Define object class to bb color mapping
color_dict = {
    'Heart': (0, 255, 0)
    }

# assuming you have a dictionary with the bounding box info:
bbox = {
    'xMin': 0.2154838709677419,
    'xMax': 0.44,
    'yMin': 0.2838709677419355,
    'yMax': 0.5083870967741936,
    'displayName': 'heart'  # object type
}

# Convert relative coordinates to absolute
height, width = 320, 320
xMin = int(bbox['xMin'] * width)
xMax = int(bbox['xMax'] * width)
yMin = int(bbox['yMin'] * height)
yMax = int(bbox['yMax'] * height)

# get color for the object type
color = color_dict.get(bbox['displayName'], (0, 255, 0))  # default to green if not found

# draw rectangle on image
cv2.rectangle(image, (xMin, yMin), (xMax, yMax), color, 2)

# Convert BGR to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# display image using matplotlib
plt.imshow(image_rgb)
plt.show()

