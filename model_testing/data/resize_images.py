import os
import cv2
import random
import numpy as np
from tqdm import tqdm 

# Run this script to resize image to 640x640 like a google street view image

image_dir = "C:/Users/morit/city-elements/model_testing/data/original_images"  
label_dir = "C:/Users/morit/city-elements/model_testing/data/labels"  
output_image_dir = "C:/Users/morit/city-elements/model_testing/data/images_resized"  
output_label_dir = "C:/Users/morit/city-elements/model_testing/data/labels_resized" 

os.makedirs(output_image_dir, exist_ok=True)
os.makedirs(output_label_dir, exist_ok=True)

IMG_SIZE = 640

image_samples = []

for img_file in tqdm(os.listdir(image_dir), desc="Processing images"):
    if img_file.endswith(('.jpg', '.png', '.jpeg')):
        img_path = os.path.join(image_dir, img_file)
        label_path = os.path.join(label_dir, img_file.replace('.jpg', '.txt').replace('.png', '.txt'))

        img = cv2.imread(img_path)
        h, w, _ = img.shape 

        resized_img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        output_img_path = os.path.join(output_image_dir, img_file)
        cv2.imwrite(output_img_path, resized_img)

        new_lines = []
        if os.path.exists(label_path):
            with open(label_path, "r") as f:
                lines = f.readlines()

            for line in lines:
                parts = line.strip().split()
                if len(parts) == 5:
                    class_id, x, y, width, height = map(float, parts)

                    x_new = x * (IMG_SIZE / w)
                    y_new = y * (IMG_SIZE / h)
                    width_new = width * (IMG_SIZE / w)
                    height_new = height * (IMG_SIZE / h)

                    new_lines.append(f"{int(class_id)} {x_new:.6f} {y_new:.6f} {width_new:.6f} {height_new:.6f}\n")

            output_label_path = os.path.join(output_label_dir, img_file.replace('.jpg', '.txt').replace('.png', '.txt'))
            with open(output_label_path, "w") as f:
                f.writelines(new_lines)

print("All images resized and labels updated!")

