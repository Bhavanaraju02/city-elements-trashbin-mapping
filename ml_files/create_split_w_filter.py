import os
import shutil
from glob import glob
from sklearn.model_selection import train_test_split
from tqdm import tqdm

# Paths to the source folders
source_folders = ["neg_samples"]

# Prepend 'city_data_raw/' to each folder name in the list
source_folders = [f"city_data_raw/{folder}" for folder in source_folders]

# Output directories
output_base = "city_data_bbox_filtered_w_neg_samples"
image_train_dir = os.path.join(output_base, "images/train")
image_val_dir = os.path.join(output_base, "images/val")
label_train_dir = os.path.join(output_base, "labels/train")
label_val_dir = os.path.join(output_base, "labels/val")

# Create the output directories
os.makedirs(image_train_dir, exist_ok=True)
os.makedirs(image_val_dir, exist_ok=True)
os.makedirs(label_train_dir, exist_ok=True)
os.makedirs(label_val_dir, exist_ok=True)

# Threshold for bounding box area (to exclude small boxes)
bbox_area_threshold = 0.0003

# Collect all images and labels
all_images = []
all_labels = []

print("Collecting image-label pairs...")

# Function to check bounding box area in a label file
def is_valid_label(label_file):
    """
    Returns True if the label file is valid (either empty or all bounding boxes 
    have an area >= bbox_area_threshold). Returns False if any bounding box 
    has an area below the threshold.
    """
    if os.path.getsize(label_file) == 0:  # Empty file is valid
        return True

    with open(label_file, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 5:
                _, x_center, y_center, width, height = map(float, parts)
                area = width * height
                if area < bbox_area_threshold:
                    return False  # Exclude the image if any bbox is too small
    return True  # Include the image if all bboxes are valid

# Iterate through the source folders to collect valid images and labels
for folder in tqdm(source_folders, desc="Processing Folders"):
    image_files = glob(os.path.join(folder, "images", "*.jpg"))  # Adjust the image extension if needed
    label_files = [os.path.join(folder, "labels", os.path.basename(img).replace(".jpg", ".txt")) for img in image_files]
    
    # Ensure that every image has a corresponding label and that the bounding boxes are valid
    for img, lbl in zip(image_files, label_files):
        if os.path.exists(lbl) and is_valid_label(lbl):  # Only add if label file exists and is valid
            all_images.append(img)
            all_labels.append(lbl)

# Perform train/val split
print("Splitting data into train and validation sets...")
train_images, val_images, train_labels, val_labels = train_test_split(
    all_images, all_labels, test_size=0.2, random_state=42
)

# Copy the files to the respective directories
print("Copying training data...")
for img, lbl in tqdm(zip(train_images, train_labels), desc="Training Data", total=len(train_images)):
    shutil.copy(img, os.path.join(image_train_dir, os.path.basename(img)))
    shutil.copy(lbl, os.path.join(label_train_dir, os.path.basename(lbl)))

print("Copying validation data...")
for img, lbl in tqdm(zip(val_images, val_labels), desc="Validation Data", total=len(val_images)):
    shutil.copy(img, os.path.join(image_val_dir, os.path.basename(img)))
    shutil.copy(lbl, os.path.join(label_val_dir, os.path.basename(lbl)))

print("Train/val split completed!")
