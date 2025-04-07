import os

# Run this script to count files in a folder

def count_files_in_folder(folder_path):
    try:
        return len([f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))])
    except FileNotFoundError:
        print("Error: Folder not found.")
        return 0
    except PermissionError:
        print("Error: Permission denied.")
        return 0

if __name__ == "__main__":
    folder_path = "city_data_bbox_filtered/images/val"
    file_count = count_files_in_folder(folder_path)
    print(f"Number of files in '{folder_path}': {file_count}")
