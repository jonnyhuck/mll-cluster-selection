# python html-output-key.py > clusters.md && pandoc -s -c skeleton.css -o clusters.html clusters.md

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pyproj import Proj, transform


def deproject(p):
	'''
	* Pe-Project (Transform) UTM coordinates to WGS84
	'''
	# transform the coordinates
	longitude, latitude = transform(Proj(init='epsg:21096'), Proj(init='epsg:4326'), p.x, p.y)
	return longitude, latitude


# get geodataframe
gdf = gpd.read_file("../results-with-omoro.shp")
	
# get and structure the dataset
ids = gdf['id'].tolist()
district = gdf['district'].tolist()
location = gdf['geometry'].tolist()
data = sorted(zip(ids, district, location),key=lambda l:l[1])

# print out data
print "# MLL Prevalance Study Cluster Data"
print "Below is a list of the selected clusters for the prevalace study. You can click to see a static satellite image and a Google Map of each area in order to make sure that there are residences there before you go. If there are not, please report this to [Jonny]('mailto:jonathan.huck@manchester.ac.uk') and he will give you a new cluster to replace it."
print
print "The static satellite image should load quickly and will let you verify that there are huts in the area. The Google Map is interactive satellite imagery that will help you plan your journey. The OpenStreetMap is an incomplete map that might contain additional details in some areas, but will be blank in others."
print
print "ID | District | Longitude | Latitude | Get Map Image | Get Google Map | Get OpenStreetMap | Get OS Map"
print "---|---|---|---|---|---|---|---"
for d in data:
	lng, lat = deproject(Point(d[2]))
	print str(d[0]) + "|" + str(d[1]) + "|" + str(lng) + "|" + str(lat) + \
	"|[click_for_satellite_image](" + "".join(["https://maps.googleapis.com/maps/api/staticmap?maptype=satellite&center=", str(lat), ",", str(lng), "&zoom=17&size=640x640&key="]) + ")" + \
	"|[click_for_Google_Map](" + "".join(["https://www.google.com/maps/@", str(lat), ",", str(lng), ",750m/data=!3m1!1e3"]) + ")" + \
	"|[click_for_OpenStreetMap](" + "".join(["https://www.openstreetmap.org/#map=17/", str(lat), "/", str(lng)]) + ")" + \
	"|[click_for_OS_Map](" + "".join(["http://huckg.is/uganda50k/#map=13/", str(lat), "/", str(lng)]) + ")"