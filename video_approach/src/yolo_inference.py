import cv2
import torch
import numpy as np 
import pandas as pd 

# load YOLO model
def load_model(model_path):
    model = torch.hub.load('WongKinYiu/yolov7', 'custom', model_path,
                           force_reload=False, trust_repo=True)
    return model

# run detection on a single frame
def detect_objects(model, frame):
    
    
    image = np.array(frame)
    if image.shape[-1] == 4:  # Handle RGBA
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    elif image.shape[-1] == 3:  # Handle RGB (convert to BGR)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # run the YOLO model
    results = model(image)

    # format the results [[bounding box], confidence, class]
    filtered_results = pd.DataFrame(results.xyxy[0].cpu().numpy(), columns=['xmin', 'ymin', 'xmax', 'ymax', 'conf', 'class'])
    return filtered_results
