"""
* This code is for the Uganda MLL project
*
* It converts a raster of population data to points (excluding 0's) and then stores the resulting
* 	points along with the name of the containing district.
*
* @author jonnyhuck
"""

from shapely.geometry import shape, mapping, Point
import rasterio, fiona

def coords2Image(a, x, y):
	"""
	* use an affine transformation to convert between coordinate space and image space
	"""
	r,c = ~a * (x, y)
	return int(r), int(c)

def image2Coords(a, col, row):
	"""
	* use an affine transformation to convert between image space and coordinate space
	"""
	return a * (col, row)
	
def getDistrict(x, y):
	"""
	* calculate the enclosing district for a point
	"""
	# make a shapely point
	p = Point(x, y)
	
	# test which district contains it and return the name
	for district in range(len(districts)):
		if districts[district].contains(p):
			return districtNames[district]
	
	# if not within any
	return "n/a"


# extract the district information fo use later
with fiona.open('../sa-districts.shp') as i:
	
	# shapefile to list
	l = list(i)
	
	# extract geometry to shapely and store in list
	districts = [shape(j['geometry']) for j in l]
	
	# extract name and store in list for later
	districtNames = [j['properties']['DNAME_2010'] for j in l]

# open dataset and retrieve data
with rasterio.open('../sa_fb_21096.tif') as src:

	# unique ID field for each point
	id = 1
	
	# get tranformation matrix
	a = src.affine
	
	# extract band 1 (only band)
	d = src.read(1)
	
	# calculate the offset (from tl to centre of cell)
	offset = src.res[0] / 2
	
	# create the file in write mode, with the required CRS and schema
	with fiona.open('../pop_points.shp', 'w', driver='ESRI Shapefile', crs={'init': 'epsg:21096'}, schema={'geometry': 'Point', 'properties': {'id': 'int', 'pop': 'int', 'district': 'str'}} ) as o:

		# loop through - if value export point
		for r in range(src.height-1):
			for c in range(src.width-1):
			
				# is there a value in that cell?
				if d[r, c] > 0:
			
					# get location
					x, y = image2Coords(a, c, r)
					
					# build point and write to output dataset
					o.write({'geometry': mapping(Point(x + offset, y - offset)),'properties': {'id': id, 'pop': d[r, c], 'district': getDistrict(x, y)}})
				
					# increment id value
					id += 1

print str(id) + " points found..."
print "Done!"