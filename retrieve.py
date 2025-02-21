import pyrpoj


transformer = Transformer.from_crs("EPSG:26915", "EPSG:4326", always_xy=True)

utm_x, utm_y = 463949.4798,4977235.225

lat, lon = transformer.tramsform(utm_x, utm_y)
print(lat, lon)