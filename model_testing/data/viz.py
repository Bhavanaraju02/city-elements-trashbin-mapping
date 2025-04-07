from ultralytics import YOLO
import torch 
import cv2
import random 
import os 

# Load the YOLOv11 model 
def load_model_yolov11(model_path):
    model = YOLO(model_path)
    return model 

yolov11_dist_ns_path = "C:/Users/morit/city-elements/model_testing/models/yolov11_dist_ns.pt"
image_dir = "C:/Users/morit/city-elements/model_testing/data/original_images"
image = "C:/Users/morit/city-elements/model_testing/image.png"
model = load_model_yolov11(yolov11_dist_ns_path)

# Get all image files
image_files = [os.path.join(image_dir,f) for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

# Select 10 random images
random_images = random.sample(image_files, min(20, len(image_files)))

# Run batched inference on a list of images
results = model(image)  # return a list of Results objects

# Process results list
for result in results:
    boxes = result.boxes  # Boxes object for bounding box outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Probs object for classification outputs
    obb = result.obb  # Oriented boxes object for OBB outputs
    result.show()  # display to screen
    result.save(filename="result.jpg")  # save to disk