import cv2
import numpy as np
from flask import Flask, request, jsonify
import base64

# Initialize Flask app
app = Flask(__name__)

# 🔹 Function to load images from the uploaded files
def load_images_from_request(files):
    images = []
    for file in files:
        # Read the image from the byte data of the uploaded file
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            return None  # If an image could not be loaded, return None
        images.append(img)
    return images

# 🔹 Function to stitch images efficiently
def stitch_images(img1, img2, img3):
    stitcher = cv2.Stitcher_create()  # OpenCV Stitcher for panorama
    status, stitched = stitcher.stitch([img1, img2, img3])

    if status == cv2.Stitcher_OK:
        return stitched
    else:
        print("Error in stitching:", status)
        return None

# 🔹 API endpoint to accept images and return the stitched result
@app.route('/stitch', methods=['POST'])
def stitch_endpoint():
    files = request.files.getlist('images')  # Expecting a list of images in 'images' field
    
    if len(files) != 3:
        return jsonify({"error": "Please upload exactly three images."}), 400
    
    # Load images from the request
    images = load_images_from_request(files)
    
    if images is None:
        return jsonify({"error": "Error loading images."}), 400
    
    left, middle, right = images
    
    # Perform stitching
    stitched_result = stitch_images(left, middle, right)

    if stitched_result is None:
        return jsonify({"error": "Error stitching images."}), 500
    
    # Convert the stitched image to a base64 string
    _, buffer = cv2.imencode('.jpg', stitched_result)
    image_bytes = buffer.tobytes()
    
    # Encode the image in base64
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    
    return jsonify({"stitched_image": encoded_image})

# Run Flask app (host 0.0.0.0 so it's accessible externally)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
