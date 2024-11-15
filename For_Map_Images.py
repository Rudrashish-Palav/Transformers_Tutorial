import requests
import matplotlib.pyplot as plt
from io import BytesIO
from PIL import Image

def get_coordinates(address, api_key):
    """Get latitude and longitude for an address using Google Maps Geocoding API."""
    geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(geocode_url)
    if response.status_code == 200:
        result = response.json()
        if result['results']:
            location = result['results'][0]['geometry']['location']
            return location['lat'], location['lng']
    raise ValueError("Could not retrieve location for the given address")

def get_map_image(lat, lng, api_key, zoom=19, size=(1000, 1000), scale=2):
    """
    Fetch a static map image centered at the specified latitude and longitude
    with a 50m:50px scale using Google Static Maps API.
    """
    map_url = (
        "https://maps.googleapis.com/maps/api/staticmap"
        f"?center={lat},{lng}&zoom={zoom}&size={size[0]}x{size[1]}"
        f"&scale={scale}&key={api_key}"
    )
    response = requests.get(map_url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise ValueError("Failed to retrieve the map image")

def plot_map(address, api_key):
    """Plot a 1000x1000 map around the address using Google Maps Static API."""
    try:
        # Step 1: Get coordinates
        lat, lng = get_coordinates(address, api_key)
        
        # Step 2: Get map image
        map_image = get_map_image(lat, lng, api_key, zoom=19)  # Adjust zoom if needed for scale
        
        # Step 3: Plot the map
        plt.figure(figsize=(10, 10))
        plt.imshow(map_image)
        plt.axis('off')  # Hide the axes
        plt.title(f"Map centered around '{address}'")
        plt.show()
    except ValueError as e:
        print(f"Error: {e}")

# Example usage
api_key = ""  # Replace with your Google Maps API key
address = "Universität Potsdam, Campus Golm, Germany"
plot_map(address, api_key)

