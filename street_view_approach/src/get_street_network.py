import osmnx as ox

def get_street_network(city_name):
    """
    Fetch the street network for a given city using OSMNx.
    Returns a graph object and a list of nodes (coordinates).
    """
    G = ox.graph_from_place(city_name, network_type='drive')
    nodes, edges = ox.graph_to_gdfs(G)
    
    return G, nodes, edges

def get_node_coordinates(G):
    """
    Extracts coordinates (latitude, longitude) for each node in the graph.
    """
    return [(data['y'], data['x']) for node, data in G.nodes(data=True)]


