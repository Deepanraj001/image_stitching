import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog

# 🔹 Function to load images
def load_images():
    file_paths = filedialog.askopenfilenames(title="Select three images", filetypes=[("Image Files", "*.jpg;*.png")])
    if len(file_paths) != 3:
        print("Please select exactly three images.")
        return None
    images = [cv2.imread(fp) for fp in file_paths]
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

# 🔹 Function to show images in Jupyter Notebook
def show_image(title, image):
    plt.figure(figsize=(10, 6))
    plt.title(title)
    plt.axis("off")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.show()

# Load images manually
images = load_images()
if images:
    left, middle, right = images

    # Perform stitching
    stitched_result = stitch_images(left, middle, right)

    # Display result
    if stitched_result is not None:
        show_image("Stitched Panorama", stitched_result)
