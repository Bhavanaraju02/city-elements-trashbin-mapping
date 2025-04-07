from geopy.distance import geodesic

def interpolate_points(p1, p2, distance):
        """Interpolate points between two coordinates with a given distance."""
        total_distance = geodesic(p1, p2).meters
        num_intervals = int(total_distance // distance)
        lat1, lon1 = p1
        lat2, lon2 = p2
        points = []
        
        for i in range(num_intervals + 1):
            if num_intervals > 0:
                fraction = i / num_intervals
                lat = lat1 + (lat2 - lat1) * fraction
                lon = lon1 + (lon2 - lon1) * fraction
                points.append((lon, lat))  
            
        return points

def sample_points_from_linestring(line, interval=10, max_dist=500):
    """
    Sample points from a LINESTRING at a specified interval (in meters).
    
    :param line: List of tuples [(lon, lat), (lon, lat), ...] representing the LINESTRING.
    :param interval: The distance between sampled points in meters (default is 10 meters).
    :return: List of sampled points as [(lon, lat), (lon, lat), ...].
    """
    sampled_points = []
    coords = list(line.coords)

    p_start = coords[0]
    p_end = coords[-1]
    total_distance = geodesic(p_start, p_end).meters
    
    # make sure that we are not going further than 500m away from the start_node
    if total_distance > max_dist:
        total_distance = max_dist
        sampled_points.extend(interpolate_points(p_start, p_end, interval))
    else:  
        sampled_points.extend(interpolate_points(p_start, p_end, interval))

    return sampled_points