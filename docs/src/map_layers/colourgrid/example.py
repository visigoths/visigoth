# -*- coding: utf-8 -*-

import os
import json

from visigoth import Diagram
from visigoth.common import Legend, Text
from visigoth.map_layers import ColourGrid
from visigoth.containers import Map
from pyproj import Transformer

class CustomProjection(object):
    """Map from pyproj to the interface for projections used for visigoth"""
    def __init__(self, name):
        self.name = name
        self.to_4326 = Transformer.from_crs(name, "EPSG:4326",always_xy=True)
        self.from_4326 = Transformer.from_crs("EPSG:4326", name,always_xy=True)

    def getName(self):
        return self.name

    def fromLonLat(self, lon_lat):
        return self.from_4326.transform(lon_lat[0], lon_lat[1],)

    def toLonLat(self, e_n):
        return self.to_4326.transform(e_n[0], e_n[1])

# load sea temperatures dataset (2D grid)
folder=os.path.split(__file__)[0]
sst = json.loads(open(os.path.join(folder,"seatemp.json")).read())

d = Diagram(fill="#D0D0D0")

# set up map with global coverage, Mollweide projection
m = Map(fill="#E0E0E0",width=512,projection=CustomProjection("ESRI:54009"),boundaries=((-180,-85),(180,85)))

# add a colourgird layer to the map using the SST data
cg = ColourGrid(sst,boundaries=((-180,-90),(180,90)))
m.addLayer(cg)

# add the map, some descriptive text and the legend to the diagram
d.add(m)
d.add(Text("sea temperatures (kelvin)"))
d.add(Legend(cg.getPalette()))

html = d.draw(format="html")
f = open("example.html", "w")
f.write(html)
f.close()

