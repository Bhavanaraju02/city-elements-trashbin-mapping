from ultralytics import YOLO
import torch 
import cv2
import random 
import os 

# This script does inference with the yolov11 model on sample data.

def load_model_yolov11(model_path):
    model = YOLO(model_path)
    return model 

yolov11_dist_ns_path = "C:/Users/morit/city-elements/model_testing/models/yolov11_dist_ns.pt"
image_dir = "C:/Users/morit/city-elements/model_testing/data/original_images"
image = "C:/Users/morit/city-elements/model_testing/image.png"
model = load_model_yolov11(yolov11_dist_ns_path)

image_files = [os.path.join(image_dir,f) for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

random_images = random.sample(image_files, min(20, len(image_files)))

results = model(image) 

for result in results:
    boxes = result.boxes  
    masks = result.masks 
    keypoints = result.keypoints  
    probs = result.probs  
    obb = result.obb  
    result.show()
    result.save(filename="result.jpg") 