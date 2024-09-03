# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 17:46:57 2024

@author: Douglas Masho
"""

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import io
from PIL import Image
import numpy as np
from ultralytics import YOLOv10


# Initialize the FastAPI app
app = FastAPI()

# Load the YOLOv10 model
model_path = "yolodetection.pt"  # Change this to the path where your model is saved
model = YOLOv10(model_path)

# Define the prediction function
def predict(image):
    # Convert the uploaded image to a format YOLOv10 can process
    image = Image.open(io.BytesIO(image)).convert("RGB")
    image = np.array(image)

    # Run the YOLOv10 model on the image
    result = model.predict(source=image, imgsz=640, conf=0.25)
    
    # Annotate the image
    annotated_img = result[0].plot()
    
    # Convert the annotated image to RGB for returning
    annotated_img = Image.fromarray(annotated_img[:, :, ::-1])
    
    # Save the image to a BytesIO object
    img_byte_arr = io.BytesIO()
    annotated_img.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    return img_byte_arr

# Define the FastAPI endpoint
@app.post("/predict/")
async def predict_image(file: UploadFile = File(...)):
    # Read the uploaded file
    image_bytes = await file.read()
    
    # Make prediction
    annotated_image = predict(image_bytes)
    
    # Return the image as a response
    return StreamingResponse(io.BytesIO(annotated_image), media_type="image/jpeg")

# Run the app using `uvicorn` if executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
