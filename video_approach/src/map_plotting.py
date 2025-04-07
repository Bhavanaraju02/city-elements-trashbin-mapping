import gmplot

def plot_on_map(locations):
    gmap = gmplot.GoogleMapPlotter(37.4275, -122.1697, 15)  # Center around your area
    for lat, lon in locations:
        gmap.marker(lat, lon, 'red', title="Trash Bin")
    gmap.draw("output/map.html")
