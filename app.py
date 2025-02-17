import cv2
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, request, jsonify
import os

# Initialize Flask app
app = Flask(__name__)

# 🔹 Function to load images from the file paths provided via HTTP request
def load_images_from_request(files):
    images = []
    for file in files:
        img = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            return None
        images.append(img)
    return images

# 🔹 Function to stitch images efficiently
def stitch_images(img1, img2, img3):
    stitcher = cv2.Stitcher_create()
    status, stitched = stitcher.stitch([img1, img2, img3])

    if status == cv2.Stitcher_OK:
        return stitched
    else:
        print("Error in stitching: ", status)
        return None

# 🔹 Function to show images (for debugging in a notebook, but for web we will just return the result)
def show_image(image):
    plt.figure(figsize=(10, 6))
    plt.axis("off")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()

# 🔹 API endpoint to accept images and return the stitched result
@app.route('/stitch', methods=['POST'])
def stitch_endpoint():
    files = request.files.getlist('images')
    
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
    
    # Convert the stitched image to a base64 string or save it and return the URL
    _, buffer = cv2.imencode('.jpg', stitched_result)
    image_bytes = buffer.tobytes()
    
    # Here we just return the image as a base64 string or save to a server path for download
    import base64
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')
    
    return jsonify({"stitched_image": encoded_image})

# Run Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
