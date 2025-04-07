import osmnx as ox

# Use this script to plot an osmnx graph of a city. 

city_name = "Lüneburg, Lower Saxony, Germany"
G = ox.graph_from_place(city_name, network_type='drive')
ox.plot_graph(G)
