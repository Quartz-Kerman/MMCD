from pyproj import Transformer
import pandas

transformer = Transformer.from_crs("EPSG:26915", "EPSG:4326", always_xy=True)
data = pandas.read_csv("sample_Ground_Site_Data.csv")

def create_node(site_name, x, y):
    lat, lon = transform_coords(x, y)
    return {'site_name': site_name, 'latitude': lat, 'longitude': lon, 'next': None}

def transform_coords(x, y):
    lon, lat = transformer.transform(x, y)
    return lat, lon

def sites_ordered(site_ids):
    nodes = []
    for site_id in site_ids:
        print(f"Processing site_id: {site_id}")
        for _, row in data.iterrows():
            site_code = row['Sitecode']
            if site_code == str(site_id):
                print(f"Match found for site_id: {site_id}")
                site_name = row['Site']
                x = row['xCentroids']
                y = row['yCentroids']
                print(f"Creating node for site_name: {site_name}, x: {x}, y: {y}")
                nodes.append(create_node(site_name, x, y))
    return nodes

def extract_zone(sitecode):
    return sitecode.split('-')[0]

def whole_quadrant(zone_number):
    nodes = []
    for _, row in data.iterrows():
        site_zone = extract_zone(row['Sitecode'])
        if site_zone == str(zone_number):
            site_name = row['Site']
            x = row['xCentroids']
            y = row['yCentroids']
            nodes.append(create_node(site_name, x, y))
    print(nodes)
    return nodes

def whole_quadrant_red(zone_number):
    nodes = []
    for _, row in data.iterrows():
        site_zone = extract_zone(row['Sitecode'])
        if site_zone == str(zone_number) and str(row['Priority']) == 'RED':
            site_name = row['Site']
            x = row['xCentroids']
            y = row['yCentroids']
            nodes.append(create_node(site_name, x, y))
    return nodes