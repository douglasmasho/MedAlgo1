# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 18:36:53 2024

@author: Douglas Masho
"""

import requests

# URL of your FastAPI endpoint
url = 'http://localhost:8000/predict/'  # Replace with your deployed URL if different

# Path to the brain scan image you want to test
image_path = 'test.jpg'  # Replace with the path to your image

# Open the image file in binary mode
with open(image_path, 'rb') as image_file:
    # Prepare the files dictionary to send as multipart/form-data
    files = {'file': image_file}
    
    # Send a POST request to the endpoint
    response = requests.post(url, files=files)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Save the annotated image received from the server
        with open('annotated_image.jpg', 'wb') as out_file:
            out_file.write(response.content)
        print("Annotated image saved as 'annotated_image.jpg'")
    else:
        print(f"Request failed with status code {response.status_code}: {response.text}")
