from pyproj import Transformer
import opencsv

transformer = Transformer.from_crs("EPSG:26915", "EPSG:4326", always_xy=True)

def sites_ordered():
    pass

def whole_quadrant():
    pass

def transform_coords(x, y):
    pass

utm_x, utm_y = 463949.4798, 4977235.225

lat, lon = transformer.transform(utm_x, utm_y)
print(lon, lat)