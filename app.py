import streamlit as st
import cv2
import numpy as np
import matplotlib.pyplot as plt

# 🔹 Function to load images from Streamlit uploader
def load_images(uploaded_files):
    images = []
    for uploaded_file in uploaded_files:
        img = cv2.imdecode(np.frombuffer(uploaded_file.read(), np.uint8), 1)
        images.append(img)
    return images

# 🔹 Function to stitch images efficiently
def stitch_images(img1, img2, img3):
    stitcher = cv2.Stitcher_create()
    status, stitched = stitcher.stitch([img1, img2, img3])
    
    if status == cv2.Stitcher_OK:
        return stitched
    else:
        return None

# 🔹 Function to display the image in Streamlit
def show_image(title, image):
    st.image(image, caption=title, use_column_width=True)

# Streamlit UI
st.title('Image Stitching Application')
st.write("Upload exactly three images to stitch them into a panorama!")

# File upload
uploaded_files = st.file_uploader("Choose three images", accept_multiple_files=True, type=["jpg", "png"])

if len(uploaded_files) == 3:
    # Load the images
    images = load_images(uploaded_files)
    left, middle, right = images
    
    # Perform stitching
    stitched_result = stitch_images(left, middle, right)

    if stitched_result is not None:
        # Display stitched result
        show_image("Stitched Panorama", stitched_result)
    else:
        st.error("There was an issue in stitching the images.")
else:
    st.warning("Please upload exactly three images to proceed.")
