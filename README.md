# mll-cluster-selection
The scripts used for cluster selection in the 2017-19 MLL Prevalance Study.

`raster2points.py` turns a raster of population counts into points at all locations > 0 and tags them with a district name from a complementary dataset.
Dependencies:

* rasterio
* fiona
* shapely

Random points were extracted from that dataset using [QGIS](https://www.qgis.org/en/site/) *(no point reinventing the wheel...)*

`html-output.py` turns the results into a HTML list including links to startic Google Satellite images allowing pre-visit site assessment.
Usage:

`python html-output.py > clusters.md && pandoc -s -c skeleton.css -o clusters.html clusters.md`

Dependencies:

* geopandas
* shapely
* pyproj

This repository includes unmdified css from [Skeleton](https://github.com/dhg/Skeleton/)
