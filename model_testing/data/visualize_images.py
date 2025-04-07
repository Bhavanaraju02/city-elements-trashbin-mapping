import os
import cv2
import random

# Paths
image_dir = "C:/Users/morit/city-elements/model_testing/data/images"  # Input images folder
label_dir = "C:/Users/morit/city-elements/model_testing/data/labels"  # Input labels folder
output_dir = "C:/Users/morit/city-elements/model_testing/data/visualized"  # Folder to save images with boxes

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Get all image files
image_files = [f for f in os.listdir(image_dir) if f.endswith(('.jpg', '.png', '.jpeg'))]

# Select 10 random images
random_images = random.sample(image_files, min(20, len(image_files)))

def draw_bounding_boxes(img_path, label_path):
    """Reads an image and its label file, draws bounding boxes, and returns the image."""
    img = cv2.imread(img_path)
    h, w, _ = img.shape  # Get image dimensions

    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) == 5:
                class_id, x_center, y_center, width, height = map(float, parts)

                # Convert YOLO format (normalized) to pixel coordinates
                x1 = int((x_center - width / 2) * w)
                y1 = int((y_center - height / 2) * h)
                x2 = int((x_center + width / 2) * w)
                y2 = int((y_center + height / 2) * h)

                # Draw rectangle
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, f"Class {int(class_id)}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    return img

# Process and save images
for img_file in random_images:
    img_path = os.path.join(image_dir, img_file)
    label_path = os.path.join(label_dir, img_file.replace('.jpg', '.txt').replace('.png', '.txt'))

    img_with_boxes = draw_bounding_boxes(img_path, label_path)

    # Save the image with bounding boxes
    output_path = os.path.join(output_dir, img_file)
    cv2.imwrite(output_path, img_with_boxes)

print(f"✅ Process complete! Images with bounding boxes saved in: {output_dir}")
