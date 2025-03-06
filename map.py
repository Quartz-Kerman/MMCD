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
    headers = { "Content-Type": "application/x-www-form-urlencoded" }
    response = requests.post(url, headers=headers, auth=(username, password), data=payload)                                                                                      
    return response.text

def get_coords(data, response):
    # Initialize an empty list to store the ordered coordinates
    ordered_coords = []
    
    # Iterate through the response and match the location names with data's coordinates
    for route in response:
        for i in range(len(route["route"])):
            address = route["route"][str(i)]["name"]
            
            # Find the matching coordinates from the 'data' list and add to the ordered list
            for entry in data:
                if entry["address"] == address:
                    lat, lng = float(entry["lat"]), float(entry["lng"])
                    ordered_coords.append((lat, lng))
                    break  # Stop once we've found the matching address
    
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


locations = [                                                                                                                                                              
        {"address": "The Hague, The Netherlands", "lat": "52.05429", "lng": "4.248618"},                                                                                   
        {"address": "Sint-Oedenrode, The Netherlands", "lat": "51.589548", "lng": "5.432482"},           
        {"address": "The Hague, The Netherlands", "lat": "52.076892", "lng": "4.26975"},                                                                       
        {"address": "Uden, The Netherlands", "lat": "51.669946", "lng": "5.61852"}                                                                                                                                                    
    ]

print(route_query(locations))
response = route_query(locations)
coords = get_coords(locations, response)
print(get_map_embed(coords))



