import os
import random
import cv2
import matplotlib.pyplot as plt

def parse_labels(label_path):
    """
    Parses a label file and returns bounding box coordinates.
    Assumes the label format: class_id x_center y_center width height (normalized).
    """
    bboxes = []
    with open(label_path, 'r') as file:
        for line in file:
            _, x_center, y_center, width, height = map(float, line.strip().split())
            bboxes.append((x_center, y_center, width, height))
    return bboxes

def denormalize_bbox(bbox, img_width, img_height):
    """
    Converts normalized bounding box coordinates to pixel values.
    """
    x_center, y_center, width, height = bbox
    x_min = int((x_center - width / 2) * img_width)
    y_min = int((y_center - height / 2) * img_height)
    x_max = int((x_center + width / 2) * img_width)
    y_max = int((y_center + height / 2) * img_height)
    return x_min, y_min, x_max, y_max

def main():
    # Define paths
    path_to_images_train = "multiple_city_data/images/train"  # Path to images folder
    path_to_labels_train = "multiple_city_data/labels/train"  # Path to labels folder
    output_path = "./labeled_images_example"           # Path to save output images

    # Create the output directory if it does not exist
    os.makedirs(output_path, exist_ok=True)

    # Get image files
    image_files = [f for f in os.listdir(path_to_images_train) if f.endswith(('.jpg', '.png'))]
    print(f"Found {len(image_files)} images.")

    # Randomly select two images
    selected_images = random.sample(image_files, 20)
    print(f"Selected images: {selected_images}")

    # Process and save images
    for img_name in selected_images:
        img_path = os.path.join(path_to_images_train, img_name)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_height, img_width, _ = img.shape

        # Parse label file
        label_name = os.path.splitext(img_name)[0] + '.txt'
        label_path = os.path.join(path_to_labels_train, label_name)

        if os.path.exists(label_path):
            bboxes = parse_labels(label_path)
            for bbox in bboxes:
                x_min, y_min, x_max, y_max = denormalize_bbox(bbox, img_width, img_height)
                cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # Draw green bounding box

        # Save the image with bounding boxes
        save_path = os.path.join(output_path, f"processed_{img_name}")
        cv2.imwrite(save_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
        print(f"Saved: {save_path}")

    print("Processing complete. Images saved in:", output_path)

if __name__ == "__main__":
    main()
