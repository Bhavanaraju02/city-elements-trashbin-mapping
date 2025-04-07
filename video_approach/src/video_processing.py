import cv2
from src.yolo_inference import detect_objects
import os 

def process_video(video_path, model, output_dir="data/output", confidence_threshold=0.9):
    
    cap = cv2.VideoCapture(video_path)
    frame_number = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # rotate 
        frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
        # detect trashbins
        detections = detect_objects(model, frame)
        
        num_trashbins = 0
        if not detections.empty:  # if we detected at least one trash bin
            for _, row in detections.iterrows():
                
                x1, y1, x2, y2 = row['xmin'], row['ymin'], row['xmax'], row['ymax']
                confidence = row['conf']
                
                # only draw bin if confidence is higher than specified threshold
                if confidence >= confidence_threshold:
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color=(0, 255, 0), thickness=2)
                    # add the confidence score as text
                    cv2.putText(frame, f"trashbin {confidence:.2f}", (int(x1), int(y1) - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    num_trashbins += 1 # increment number of trashbins drawn to only save images where we drew a trashbin
            
            # save frame if we drew at least one trashbin
            if num_trashbins > 0:
                output_path = os.path.join(output_dir, f"frame_{frame_number}.jpg")
                cv2.imwrite(output_path, frame)
        
        frame_number += 1

    cap.release()
    print(f"Processing complete. Frames with detections saved to '{output_dir}'.")

