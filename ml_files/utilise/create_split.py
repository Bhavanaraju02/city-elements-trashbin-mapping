import os
import shutil
from glob import glob
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# Run this file to create a train/val split 
# File paths are hardcoded

'''source_folders = ["bremen_images", "hamburg_images", "hannover_images", "berlin_images", "dresden_images",
                  "essen_images", "frankfurt_images", "munich_imaches", "nürnberg_images", 'stuttgart_images', 
                  "lübeck_images", "lüneburg_images", "schwerin_images", "neg_samples"]'''
                  
source_folders = ["neg_samples"]



source_folders = [f"city_data_raw/{folder}" for folder in source_folders]


output_base = "city_data_w_neg_samples"
image_train_dir = os.path.join(output_base, "images/train")
image_val_dir = os.path.join(output_base, "images/val")
label_train_dir = os.path.join(output_base, "labels/train")
label_val_dir = os.path.join(output_base, "labels/val")


os.makedirs(image_train_dir, exist_ok=True)
os.makedirs(image_val_dir, exist_ok=True)
os.makedirs(label_train_dir, exist_ok=True)
os.makedirs(label_val_dir, exist_ok=True)

all_images = []
all_labels = []

print("Collecting image-label pairs...")
for folder in tqdm(source_folders, desc="Processing Folders"):
    image_files = glob(os.path.join(folder, "images", "*.jpg"))  
    label_files = [os.path.join(folder, "labels", os.path.basename(img).replace(".jpg", ".txt")) for img in image_files]
    
    for img, lbl in zip(image_files, label_files):
        if os.path.exists(lbl):
            all_images.append(img)
            all_labels.append(lbl)

print("Splitting data into train and validation sets...")
train_images, val_images, train_labels, val_labels = train_test_split(
    all_images, all_labels, test_size=0.2, random_state=42
)

print("Copying training data...")
for img, lbl in tqdm(zip(train_images, train_labels), desc="Training Data", total=len(train_images)):
    shutil.copy(img, os.path.join(image_train_dir, os.path.basename(img)))
    shutil.copy(lbl, os.path.join(label_train_dir, os.path.basename(lbl)))

print("Copying validation data...")
for img, lbl in tqdm(zip(val_images, val_labels), desc="Validation Data", total=len(val_images)):
    shutil.copy(img, os.path.join(image_val_dir, os.path.basename(img)))
    shutil.copy(lbl, os.path.join(label_val_dir, os.path.basename(lbl)))

print("Train/val split completed!")
