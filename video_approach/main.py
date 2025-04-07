from src.yolo_inference import load_model
from src.video_processing import process_video
from src.image_processing import process_image
from src.gps_processing import extract_gps_metadata, triangulate_location
#from src.map_plotting import plot_on_map

if __name__ == "__main__":
    # Load model
    #model_path = "models/model_01.pt"
    #model = load_model(model_path)

    # Process video
    #video_path = "data/video.MOV"
    #process_video(video_path, model)

    # Process image
    image_path = "data/test1.png"
    #process_image(image_path, model)
    
    # Extract GPS metadata (mocked for now)
    gps_data = extract_gps_metadata(image_path)
    # Triangulate trash bin locations (mocked for now)
    #trash_bin_locations = [(37.4275, -122.1697)]  # Placeholder
    
    # Plot on map
    #plot_on_map(trash_bin_locations)
