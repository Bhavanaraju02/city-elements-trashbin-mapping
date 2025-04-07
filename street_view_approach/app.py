import streamlit as st
import folium
from streamlit_folium import st_folium
from src.detect_trashbin import load_model, predict_trashbins, draw_boxes
from src.fetch_street_view import fetch_street_view_image
from src.create_map import add_pin, visualize_path
from shapely.geometry import LineString
from src.get_street_network import get_street_network
from src.sample_points import sample_points_from_linestring
import os
from streamlit_folium import folium_static
import osmnx as ox
import pandas as pd
from geopy.geocoders import Nominatim

# This file is responsible for the streamlit layout and going through the detection pipeline.

st.set_page_config(layout="wide")
st.title("Trash Bin Detection and Mapping")
st.sidebar.header("Input Parameters")
city_name = st.sidebar.text_input("City Name", "Lüneburg, Germany")
geolocator = Nominatim(user_agent="sample@email.com") # Put in your email here
location = geolocator.geocode(city_name)

if location:
    start_lat = location.latitude
    start_lon = location.longitude
    st.sidebar.write(f"**Detected Coordinates:** {start_lat}, {start_lon}")
else:
    start_lat = st.sidebar.number_input("Start Latitude", value=53.551086, format="%.6f")
    start_lon = st.sidebar.number_input("Start Longitude", value=9.993682, format="%.6f")
    st.sidebar.warning("City not found. Please enter latitude and longitude manually.")

radius = st.sidebar.slider("Traversal Radius (meters)", 100, 1000, 150)
interval = st.sidebar.slider("Sampling Interval (meters)", 5, 50, 15)
confidence = st.sidebar.slider("Detect Trashbins at Confidence level of:",0.0, 1.0, 0.05)

processed_points = []
points_with_trashbins = []
trashbin_count = 0
# Not needed anymore
'''pins_file = "pins.json"
trashbin_map_file = "map_with_pin.html"
traversal_map_file = "traversal_map.html"
'''
col1, col2 = st.columns([3, 3])  

with col1:
    st.write("Traversal Progress")
    traversal_map_placeholder = folium_static(
        folium.Map(location=[start_lat, start_lon], zoom_start=15),
        width=500,
        height=400, 
    )
    progress_placeholder = st.empty()

with col2:
    st.write("Trashbin Map")
    trashbin_map_placeholder = folium_static(
        folium.Map(location=[start_lat, start_lon], zoom_start=15),
        width=500,
        height=400,  
    )
    count_placeholder = st.empty()

button_placeholder = st.empty()

if st.button("Start Detection Pipeline"):
    st.write("Loading model...")
    model_path = "C:/Users/morit/city-elements/street_view_approach/models/yolov11_dist.pt"
    model = load_model(model_path)
    st.write("Fetching street network...")
    G, nodes, edges = get_street_network(city_name)
    subgraph = ox.graph_from_point((start_lat, start_lon), dist=radius, network_type="all")
    edges_gdf = ox.graph_to_gdfs(subgraph, nodes=False, edges=True)
    edges_gdf.reset_index(inplace=True)
    st.write("Sampling points...")
    sampled_points = []
    for _, edge in edges_gdf.iterrows():
        if isinstance(edge.geometry, LineString):
            sampled_points.extend(sample_points_from_linestring(edge.geometry, interval))

    st.write("Detecting trash bins and updating maps...")
    total_points = len(sampled_points)

    for point in sampled_points:
        lon, lat = point
        file_name = f"{lon}_{lat}.jpg"
        visualize_path(lat, lon, processed_points, output_file=traversal_map_file)

        processed_points.append((lon, lat))
        traversal_map_placeholder.empty()
        m1 = folium.Map(location=[start_lat, start_lon], zoom_start=15)
        for lat, lon in processed_points:
            folium.Marker(location=[lat, lon], color='red', popup=f"Point: ({lat}, {lon})").add_to(m1)
        with col1:
            traversal_map_placeholder = folium_static(
                m1,
                width=500,
                height=400  
            )
            progress_percentage = (len(processed_points) / total_points) * 100
            progress_placeholder.write(f"**Progress:** {len(processed_points)}/{total_points} ({progress_percentage:.2f}%)")

        for heading in range(0, 360, 90):
            fetch_street_view_image(lat, lon, heading=heading, size="640x640", file_name=f"{heading}_{file_name}")
            image_path = f"C:/Users/morit/city-elements/street_view_approach/data/street_view_images/{heading}_{file_name}"
            predictions = predict_trashbins(model, image_path)

            if predictions.size > 0:
                box = draw_boxes(image_path, predictions, confidence_threshold=confidence)
                if box:
                    trashbin_map_placeholder.empty()
                    trashbin_count += 1
                    points_with_trashbins.append(point)
                    m2 = folium.Map(location=[start_lat, start_lon], zoom_start=15)
                    for lat, lon in points_with_trashbins:
                        image_url = f"app/static/{heading}_{file_name}"
                        folium.Marker(location=[lat, lon], popup=f'<a href="{image_url}" target="_blank">View Trashbin Image</a>').add_to(m2)
                    with col2:
                        trashbin_map_placeholder = folium_static(
                            m2,
                            width=500,
                            height=400 
                        )
                        count_placeholder.write(f"**Total Trash Bins Detected:** {trashbin_count}")
            else:
                os.remove(image_path)
