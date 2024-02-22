import pandas as pd
import folium
from collections import Counter
from branca.colormap import LinearColormap
import numpy as np

def parse_gps(gps_str):
    # Parses the GPS coordinates from the string.
    try:
        lat, lon = map(float, gps_str.split(','))
        return lat, lon
    except ValueError:
        return None

# Load your data
df = pd.read_csv('flights.csv')  # Replace with your CSV file path

# Parse the GPS coordinates
df['Departure Coordinates'] = df['Departure GPS'].apply(parse_gps)
df['Arrival Coordinates'] = df['Arrival GPS'].apply(parse_gps)

# Combine departure and arrival coordinates
coords_list = df['Departure Coordinates'].dropna().tolist() + df['Arrival Coordinates'].dropna().tolist()

# Count the frequency of each coordinate
coords_freq = Counter(coords_list)

# Define a custom color gradient
color_map = LinearColormap(['red', 'yellow', 'green'], vmin=min(coords_freq.values()), vmax=max(coords_freq.values()))

# Create a map centered on the average of the coordinates
average_lat = sum(coord[0] for coord in coords_list) / len(coords_list)
average_lon = sum(coord[1] for coord in coords_list) / len(coords_list)
mymap = folium.Map(location=[average_lat, average_lon], zoom_start=2)  # Adjust zoom_start as needed

# Add circles with gradient-like effect based on frequency
for coord, freq in coords_freq.items():
    color = color_map(freq)
    opacity = np.clip(0.3 + 0.3 * (1 - freq / max(coords_freq.values())), 0, 0.9)  # Adjust opacity based on frequency
    folium.CircleMarker(location=coord, radius=9, color=None, fill=True, fill_color=color, fill_opacity=opacity, weight=0).add_to(mymap)

# Add the color map legend
color_map.caption = 'Frequency'
mymap.add_child(color_map)

# Increase the font size of the legend labels
mymap.get_root().html.add_child(folium.Element("<style>.leaflet-control.leaflet-control-legend .leaflet-control-legend-caption {font-size: 64px !important;}</style>"))

# Save the map to an HTML file
mymap.save('heatmap.html')
