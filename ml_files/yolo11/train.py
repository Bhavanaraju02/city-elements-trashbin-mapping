from ultralytics import YOLO
 
model = YOLO("yolo11m.pt")

model.train(data="custom.yaml", #path to yaml file  
           imgsz=640, #image size for training  
           batch=8, #number of batch size  
           epochs=400, #number of epochs  
           device=0) #device ‘0’ if gpu else ‘cpu’