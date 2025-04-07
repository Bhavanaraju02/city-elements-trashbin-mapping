import folium
from folium import Map, CircleMarker
import json
import os


def add_pin(longitude, latitude, map_file="map_with_pin.html", data_file="pins.json"):
    """
    Add a pin to the map, regenerating the map entirely after each pin is added.

    Parameters:
    - latitude (float): Latitude of the new pin.
    - longitude (float): Longitude of the new pin.
    - map_file (str): Path to the HTML file for the map.
    - data_file (str): Path to the JSON file for storing pins.
    """
    if os.path.exists(data_file):
        with open(data_file, "r") as f:
            pins = json.load(f)
    else:
        pins = []
    pins.append({"latitude": latitude, "longitude": longitude})

    with open(data_file, "w") as f:
        json.dump(pins, f)

    if pins:
        center = [pins[0]["latitude"], pins[0]["longitude"]]
    else:
        center = [latitude, longitude]
    mymap = folium.Map(location=center, zoom_start=15)

    for pin in pins:
        folium.Marker([pin["latitude"], pin["longitude"]], popup="Trashbin detected!").add_to(mymap)
    mymap.save(map_file)
    print(f"Map has been updated and saved as {map_file}")


def visualize_path(lat, lon, processed_points, output_file="traversal_map.html"):
    """
    Visualize the traversal with the current location and previously processed points on a map using Folium.

    :param current_point: Tuple (lon, lat) representing the current location.
    :param processed_points: List of previously processed points [(lon, lat), ...].
    :param output_file: Path to save the HTML file of the map.
    """
    center = [lon, lat]
    m = Map(location=center, zoom_start=15)

    for point in processed_points:
        CircleMarker(
            location=[point[1], point[0]],
            radius=5,
            color="blue",
            fill=True,
            fill_color="blue",
            fill_opacity=0.8,
            popup=f"Processed Point: ({point[1]}, {point[0]})",
        ).add_to(m)

    CircleMarker(
        location=[lon, lat],
        radius=7,
        color="red",
        fill=True,
        fill_color="red",
        fill_opacity=0.8,
        popup=f"Current Point: ({lon}, {lat})",
    ).add_to(m)

    m.save(output_file)
    print(f"Traversal map updated and saved to {output_file}")



