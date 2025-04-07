import os
import numpy as np
import matplotlib.pyplot as plt

# Paths to the labels folder
labels_path = "/home/moritz.burmester/city-dev/city_data_no_neg_samples/labels/train"
output_plot_path_full = "bounding_box_distribution_full.png"  # Full distribution plot
output_plot_path_zoomed = "bounding_box_distribution_zoomed.png"  # Zoomed-in plot

# List to store bounding box areas
bbox_areas = []

# Iterate through label files
for label_file in os.listdir(labels_path):
    if label_file.endswith(".txt"):  # Process only .txt files
        with open(os.path.join(labels_path, label_file), "r") as f:
            for line in f:
                # Parse the YOLO annotation line: class x_center y_center width height
                parts = line.strip().split()
                if len(parts) == 5:
                    _, _, _, width, height = map(float, parts)
                    # Compute the area of the bounding box
                    area = width * height
                    bbox_areas.append(area)

# Convert to a NumPy array for easier manipulation
bbox_areas = np.array(bbox_areas)

# Check if there are any bounding box areas
if len(bbox_areas) > 0:
    # Plot the full distribution of bounding box areas
    plt.figure(figsize=(10, 6))
    plt.hist(bbox_areas, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
    plt.title("Full Distribution of Bounding Box Areas", fontsize=16)
    plt.xlabel("Bounding Box Area (normalized)", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(output_plot_path_full, dpi=300)
    print(f"Full distribution plot saved as '{output_plot_path_full}'")
    plt.show()

    # Plot the zoomed-in distribution of bounding box areas (0 to 0.05)
    plt.figure(figsize=(10, 6))
    plt.hist(bbox_areas, bins=2000, color='lightcoral', edgecolor='black', alpha=0.7)
    plt.title("Zoomed-In Distribution of Bounding Box Areas (0 to 0.05)", fontsize=16)
    plt.xlabel("Bounding Box Area (normalized)", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xlim(0, 0.002)  # Zoom in to the range 0 to 0.05 on the x-axis
    plt.savefig(output_plot_path_zoomed, dpi=300)
    print(f"Zoomed-in plot saved as '{output_plot_path_zoomed}'")
    plt.show()

    # Print summary statistics for additional insight
    print(f"Number of bounding boxes: {len(bbox_areas)}")
    print(f"Mean bounding box area: {np.mean(bbox_areas):.6f}")
    print(f"Median bounding box area: {np.median(bbox_areas):.6f}")
    print(f"Min bounding box area: {np.min(bbox_areas):.6f}")
    print(f"Max bounding box area: {np.max(bbox_areas):.6f}")
else:
    print("No bounding boxes found in the label files.")
