import numpy as np
from pymediainfo import MediaInfo

def extract_gps_metadata(video_path):
    media_info = MediaInfo.parse(video_path)
    metadata = {}
    
    for track in media_info.tracks:
        #print(track.track_type)
        if track.track_type == "General":
            print(track.to_data())
            metadata["duration"] = track.duration
        if track.track_type == "Video":
            metadata["frame_rate"] = track.frame_rate
            metadata["width"] = track.width
            metadata["height"] = track.height
        if track.track_type == "Image":
            print(track.to_data())
 

    return metadata


def triangulate_location(gps_frame1, gps_frame2, bbox1, bbox2):
    # Apply triangulation using GPS metadata and bounding box offsets
    # (This will likely involve some geometric transformations)
    pass
