from ultralytics import YOLO
import torch 
import cv2

# This script calculates metrics on a test set for the YOLOv7 and YOLOV11 models

def load_model_yolov7(model_path):
    model = torch.hub.load('WongKinYiu/yolov7', 'custom', model_path,
                        force_reload=False, trust_repo=True)
    return model

def load_model_yolov11(model_path):
    model = YOLO(model_path)
    return model 

yolov7_path = "C:/Users/morit/city-elements/model_testing/models/yolov7_normal_ns.pt"
yolov11_normal_path = "C:/Users/morit/city-elements/model_testing/models/yolov11_normal.pt"
yolov11_normal_ns_path = "C:/Users/morit/city-elements/model_testing/models/yolov11_normal_ns.pt"
yolov11_dist_path = "C:/Users/morit/city-elements/model_testing/models/yolov11_dist.pt"
yolov11_dist_ns_path = "C:/Users/morit/city-elements/model_testing/models/yolov11_dist_ns.pt"

yolov11 = load_model_yolov11(yolov11_dist_ns_path)

metrics = yolov11.val(data="C:/Users/morit/city-elements/model_testing/custom.yaml")
print(metrics.box.map)

