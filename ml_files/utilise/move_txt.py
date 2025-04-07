import os
import shutil

# Run this script to move text files

def move_txt_files(source_folder, destination_folder):
    os.makedirs(destination_folder, exist_ok=True)
    for file in os.listdir(source_folder):
        if file.endswith(".txt"):
            src_path = os.path.join(source_folder, file)
            dest_path = os.path.join(destination_folder, file)
            
            shutil.move(src_path, dest_path)
            print(f"Moved: {file}")
    
    print("All .txt files have been moved.")

source_folder = "/home/moritz.burmester/city-dev/neg_sample_images/images"
destination_folder = "/home/moritz.burmester/city-dev/neg_sample_images/labels"

move_txt_files(source_folder, destination_folder)