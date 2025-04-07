import torch
from PIL import Image
import numpy as np
import cv2
import os 
from src.create_map import add_pin
from ultralytics import YOLO


# This script is responsible for detecting trashbins on an image file and drawing
# a bounding box on them. 

output_dir = "C:/Users/morit/city-elements/street_view_approach/data/detected"

'''def load_model(model_path):
    model = torch.hub.load('WongKinYiu/yolov7', 'custom', model_path,
                        force_reload=False, trust_repo=True)
    return model'''

def load_model(model_path):
    model = YOLO(model_path)
    return model 

def predict_trashbins(model, image_path):
    image = Image.open(image_path)
    img = np.array(image)
    if img.shape[-1] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)


    results = model(img)
    for r in results:
        boxes = r.boxes
    # format the results [[bounding box], confidence, class]
    conf = boxes.conf.cpu().numpy()  
    _ = boxes.cls.cpu().numpy()   
    xyxy = boxes.xyxy.cpu().numpy()
    filtered_results = np.hstack((xyxy, conf[:, None], _[:, None]))
    print(filtered_results)
    return filtered_results

def draw_boxes(image_path, predictions, confidence_threshold=0.3):
    img = cv2.imread(image_path)

    num_trashbins = 0
    for pred in predictions:
        # extract bbox coords and confidence score 
        x1, y1, x2, y2, confidence, class_id = pred

        if confidence >= confidence_threshold:
            # draw rectangle if confidence score surpasses threshold 
            cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv2.putText(img, f"trashbin {confidence:.2f}", (int(x1), int(y1) - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            num_trashbins += 1
            
    if num_trashbins > 0:
        # save image with correct filename and heading
        file_name_heading = image_path.split('/')[-1]
        print(f"Trashbins detected at location {file_name_heading}")
        print(f"Number of Trashbins: {num_trashbins}")
        output_image = f"C:/Users/morit/city-elements/street_view_approach/static/{file_name_heading}"
        cv2.imwrite(output_image, img)
        parts = file_name_heading.split("_")
        latitude = float(parts[1])
        longitude = float(parts[2].replace(".jpg", ""))
        return True
    
    else: 
        os.remove(image_path)
        return False