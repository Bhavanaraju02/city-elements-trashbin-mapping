import os
import numpy as np 
import osmnx as ox
import geopandas as gpd
from geopy.distance import geodesic
from shapely.geometry import LineString
from src.fetch_street_view import fetch_street_view_image 
from src.detect_trashbin import load_model, predict_trashbins, draw_boxes
from src.get_street_network import get_street_network, get_node_coordinates
from src.create_map import visualize_path
from src.sample_points import interpolate_points, sample_points_from_linestring


# Initialize variables
city_name = "Hamburg, Germany"
model_path = "C:/Users/morit/city-elements/street_view_approach/models/yolov11_dist.pt"
output_dir = "C:/Users/morit/city-elements/street_view_approach/data/street_view_images"
detected_dir = "C:/Users/morit/city-elements/street_view_approach/data/detected"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(detected_dir, exist_ok=True)

# Load YOLOv11 model
model = load_model(model_path)

# Fetch street network for the city
G, nodes, edges = get_street_network(city_name)

# Extract node coordinates
node_coordinates = get_node_coordinates(G)

# Your given coordinates (latitude, longitude)
#lüneburg
#start_lat = 53.24788889
#start_lon = 10.41611111
#hannover
#start_lat = 52.37588889
#start_lon = 9.73200000
#Hamburg
start_lat = 53.551086
start_lon = 9.993682

'''start_node = ox.distance.nearest_nodes(G, X=start_lon, Y=start_lat)
print(f"Start node: {start_node}")
neighbors = list(G.neighbors(start_node))

# Extract edges from the graph
edges_gdf = ox.graph_to_gdfs(G, nodes=False, edges=True)
edges_gdf.reset_index(inplace=True)
# Find all edges connected to the start node
edges_from_start_node = []
for neighbor in neighbors:
    # Get the edge (street) between the start node and the neighbor node
    edge = edges_gdf[edges_gdf['u'] == start_node][edges_gdf['v'] == neighbor]
    if not edge.empty:
        edges_from_start_node.append(edge.iloc[0])
print(edges_from_start_node)
sampled_points = []
for edge in edges_from_start_node:
    edge_geometry = edge.geometry
    sampled_points.extend(sample_points_from_linestring(edge_geometry, interval=15))  # 15 meters interval
print(sampled_points)'''

# fetch subgraph within a 500-meter radius of the starting location
subgraph = ox.graph_from_point((start_lat, start_lon), dist=150, network_type='all')

# extract edges from the subgraph
edges_gdf = ox.graph_to_gdfs(subgraph, nodes=False, edges=True)
edges_gdf.reset_index(inplace=True)

# List to store sampled points
sampled_points = []

# Iterate through each edge in the subgraph and sample points
for _, edge in edges_gdf.iterrows():
    edge_geometry = edge.geometry
    if isinstance(edge_geometry, LineString):  # Ensure the geometry is a LINESTRING
        sampled_points.extend(sample_points_from_linestring(edge_geometry, interval=15))
        

processed_points = []
# Print sampled points (latitude, longitude)
for point in sampled_points:
    # Fetch Google Street View Image at the sampled point
    file_name = f"{point[0]}_{point[1]}.jpg"
    # take pictures every 90 degrees
    visualize_path(point[0], point[1], processed_points=processed_points)
    processed_points.append((point[1], point[0]))
    for heading in range(0, 360, 90):
        fetch_street_view_image(point[0], point[1], heading=heading, size="640x640", file_name=f"{heading}_{file_name}")
        image_path = f"C:/Users/morit/city-elements/street_view_approach/data/street_view_images/{heading}_{file_name}"
        # Run YOLO object detection
        predictions = predict_trashbins(model, image_path)
        if predictions.size > 0:
            draw_boxes(image_path, predictions, confidence_threshold=0.8)
        else: 
            os.remove(image_path)    
   





