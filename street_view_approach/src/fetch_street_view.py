import os
import requests

# API KEY
API_KEY = "YOUR API KEY HERE"

BASE_URL = "https://maps.googleapis.com/maps/api/streetview"

OUTPUT_DIR = "C:/Users/morit/city-elements/street_view_approach/data/street_view_images"

def fetch_street_view_image(lat, lng, heading=0, pitch=0, fov=60, size="640x640", source='outdoor', file_name="image.jpg"):
    """
    Fetch a Street View image for a given location and save it locally.

    :param lat: Latitude of the location
    :param lng: Longitude of the location
    :param heading: Camera heading (in degrees)
    :param pitch: Camera pitch (in degrees)
    :param fov: Field of view (in degrees)
    :param size: Image size (width x height, max 640x640)
    :param file_name: Name of the file to save the image
    """
    params = {
        "size": size,
        "location": f"{lat},{lng}",
        "heading": heading,
        "pitch": pitch,
        "fov": fov,
        "source": source,
        "key": API_KEY
    }
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        file_path = os.path.join(OUTPUT_DIR, file_name)
        with open(file_path, "wb") as file:
            file.write(response.content)
    else:
        print(f"Failed to fetch image. HTTP Status: {response.status_code}")
