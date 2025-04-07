import os
import shutil


# Run this script to check whether some images have empty labels

labels_folder_path = "/home/moritz.burmester/city-dev/city_data_no_neg_samples/labels/val"
images_folder_path = "/home/moritz.burmester/city-dev/city_data_no_neg_samples/images/val"
destination_folder_img = "/home/moritz.burmester/city-dev/neg_sample_images/images"
destination_folder_lbl = "/home/moritz.burmester/city-dev/neg_sample_images/labels"

os.makedirs(destination_folder_img, exist_ok=True)
os.makedirs(destination_folder_lbl, exist_ok=True)

label_files = os.listdir(labels_folder_path)

for label_file in label_files:
    label_path = os.path.join(labels_folder_path, label_file)
    
    if os.path.isfile(label_path) and os.path.getsize(label_path) == 0:
   
        base_name = os.path.splitext(label_file)[0]  
        image_file = None
        

        for ext in ['.jpg', '.png', '.jpeg', '.bmp', '.tiff']:
            potential_image_path = os.path.join(images_folder_path, f"{base_name}{ext}")
            if os.path.exists(potential_image_path):
                image_file = potential_image_path
                break

        if image_file:
            shutil.move(label_path, os.path.join(destination_folder_lbl, os.path.basename(label_path)))
            shutil.move(image_file, os.path.join(destination_folder_img, os.path.basename(image_file)))
            print(f"Moved: {label_file} and {os.path.basename(image_file)}")

print("Processing complete.")
