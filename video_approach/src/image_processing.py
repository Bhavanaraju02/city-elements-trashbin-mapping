import cv2
from src.yolo_inference import detect_objects
import os

def process_image(image_path, model, output_dir="data/output", confidence_threshold=0):
    # read the input image
    image = cv2.imread(image_path)
    
    if image is None:
        print(f"Error: Could not read the image from {image_path}")
        return
    
    # detect trashbins in the image
    detections = detect_objects(model, image)
    
    num_trashbins = 0
    if not detections.empty:  # if we detected at least one trash bin
        for _, row in detections.iterrows():
            # get the bounding box coordinates and confidence
            x1, y1, x2, y2 = row['xmin'], row['ymin'], row['xmax'], row['ymax']
            confidence = row['conf']
            print(confidence)
            
            # only draw the bounding box if the confidence is above the threshold
            if confidence >= confidence_threshold:
                cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color=(0, 255, 0), thickness=2)
                # add the confidence score as text above the bounding box
                cv2.putText(image, f"trashbin {confidence:.2f}", (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                num_trashbins += 1  # increment number of trashbins detected
    
    # save the image if we drew at least one trashbin
    if num_trashbins > 0:
        output_path = os.path.join(output_dir, "processed_image.jpg")
        cv2.imwrite(output_path, image)
        print(f"Processed image saved to '{output_path}'")
    else:
        print("No trashbins detected in the image.")
