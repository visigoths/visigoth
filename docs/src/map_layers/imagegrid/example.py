# -*- coding: utf-8 -*-

import os
import json
import math

from visigoth import Diagram
from visigoth.common import Legend, Text
from visigoth.map_layers import ImageGrid, Geoimport
from visigoth.containers import Map, Box
from visigoth.utils.colour.colour_manager import ContinuousColourManager
from visigoth.utils.httpcache import HttpCache
from pyproj import Transformer

height = 700 # cover lats from -70 to 70 @0.2 deg
width = 1800 # cover lons from -180 to 180 @0.2 deg

lat_spacing = 0.2
lon_spacing = 0.2

# work out the centers of each cell, first the latitudes
lats = [-70+i+lat_spacing*0.5 for i in range(height)]

# then the longitudes
lons = [-180+i+lon_spacing*0.5 for i in range(width)]

r = [[int(255*col/width) for col in range(width)] for row in range(height)]
g = [[int(255*row/height) for col in range(width)] for row in range(height)]
b = [[int(255*(row/height)*(1-(col/width))) for col in range(width)] for row in range(height)]
a = [[int(row+col)%255 for col in range(width)] for row in range(height)]

d = Diagram()

m = Map(fill="#E0E0E0",width=512,boundaries=((-180,-70),(180,70)))

hc = HttpCache()
geojson_path = hc.fetch("https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json",returnPath=True)
gi = Geoimport(geojson_path,line_style=lambda p:{"stroke-width":1,"stroke":"black"},polygon_style=lambda p:{"fill":"#606060"})
m.add(gi)

# add an imagegrid layer to the map using the red,green,blue and alpha channel data
cg = ImageGrid(r=r,g=g,b=b,a=a,lats=lats,lons=lons,sharpen=True)
m.add(cg)

# add the map, some descriptive text and the legend to the diagram
b = Box(m,corner_radius=5,padding=5)

d.add(b)

html = d.draw(format="html")
f = open("example.html", "w")
f.write(html)
f.close()

