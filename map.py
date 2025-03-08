import requests                                                                                                                                                            
import json          
import googlemaps                                                                                                                                                      

def route_query(locations):
    url = "https://api.routexl.com/tour/"
    username = "quartzkerman"
    routexlkey = open("routexl_auth.txt", "r")
    for line in routexlkey:
        password = line
    payload = "locations=" + json.dumps(locations)
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, headers=headers, auth=(username, password), data=payload)
    return response.json()

def get_coords(data, response):
    ordered_coords = []
    for i in range(len(response["route"])):
        address = response["route"][str(i)]["name"]
        for entry in data:
            if entry["address"] == address:
                lat, lng = float(entry["lat"]), float(entry["lng"])
                ordered_coords.append((lat, lng))
                break
    return ordered_coords

def get_map_embed(coords):
    base_url = "https://www.google.com/maps/embed/v1/directions"
    gmapskey = open("gmaps_auth.txt", "r")
    for line in gmapskey:
        api_key = line
    origin = f"{coords[0][0]},{coords[0][1]}"
    destination = f"{coords[-1][0]},{coords[-1][1]}"
    waypoints = "|".join([f"{lat},{lng}" for lat, lng in coords[1:-1]])
    maps_url = f"{base_url}?key={api_key}&origin={origin}&destination={destination}&waypoints={waypoints}&mode=driving"
    return maps_url

