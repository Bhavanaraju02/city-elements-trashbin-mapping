import os
import shutil

def move_txt_files(source_folder, destination_folder):
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # Iterate over all files in the source folder
    for file in os.listdir(source_folder):
        # Check if the file is a .txt file
        if file.endswith(".txt"):
            # Construct the full path for source and destination
            src_path = os.path.join(source_folder, file)
            dest_path = os.path.join(destination_folder, file)
            
            # Move the file
            shutil.move(src_path, dest_path)
            print(f"Moved: {file}")
    
    print("All .txt files have been moved.")

# Example usage
source_folder = "/home/moritz.burmester/city-dev/neg_sample_images/images"
destination_folder = "/home/moritz.burmester/city-dev/neg_sample_images/labels"

move_txt_files(source_folder, destination_folder)