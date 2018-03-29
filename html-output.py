# python html-output.py > clusters.md && pandoc -s -c skeleton.css -o clusters.html clusters.md

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


# INSERT YOUR GOOGLE MAPS STATIC API KEY HERE
apikey = ""

# get geodataframe
gdf = gpd.read_file("../results2.shp")

# get and structure the dataset
ids = gdf['id'].tolist()
district = gdf['district'].tolist()
location = gdf['geometry'].tolist()
data = sorted(zip(ids, district, location),key=lambda l:l[1])

# print out data
print "# MLL Prevalance Study Cluster Data"
print "Below is a list of the selected clusters for the prevalace study. You can click to see a map of each area in order to make sure that there are residences there before you go. If there are not, please report this to [Jonny]('mailto:jonathan.huck@manchester.ac.uk') and he will give you a new cluster to replace it."
print
print "ID | District | Longitude | Latitude | Get Map"
print "---|---|---|---|---"
for d in data:
	lng, lat = deproject(Point(d[2]))
	print str(d[0]) + "|" + str(d[1]) + "|" + str(lng) + "|" + str(lat) + "|[click here for map](" + "".join(["https://maps.googleapis.com/maps/api/staticmap?maptype=satellite&center=", str(lat), ",", str(lng), "&zoom=17&size=640x640&key=", apikey]) + ")"