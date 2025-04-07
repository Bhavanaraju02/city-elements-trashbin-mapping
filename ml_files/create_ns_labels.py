import os
import shutil

# Use this script to create empty labels for images without trashbins
# File paths are hardcoded

def process_images(folders, output_images_folder, output_labels_folder):
    os.makedirs(output_images_folder, exist_ok=True)
    os.makedirs(output_labels_folder, exist_ok=True)


    counter = 1


    for folder in folders:
        for filename in os.listdir(folder):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                new_name = f"neg_sample_{counter}"
                src_image_path = os.path.join(folder, filename)
                shutil.copyfile(src_image_path, dest_image_path)

                dest_label_path = os.path.join(output_labels_folder, f"{new_name}.txt")
                with open(dest_label_path, "w") as f:
                    pass  

                print(f"Processed: {filename} -> {new_name}.jpg")
                counter += 1

    print(f"Finished processing {counter - 1} images.")

# Example usage
folders = [
    "/home/moritz.burmester/city-dev/neg_sample_images/images", 
    "/home/moritz.burmester/city-dev/no_trashbin"
]
output_images_folder = "/home/moritz.burmester/city-dev/neg_samples/images"
output_labels_folder = "/home/moritz.burmester/city-dev/neg_samples/labels"

process_images(folders, output_images_folder, output_labels_folder)
