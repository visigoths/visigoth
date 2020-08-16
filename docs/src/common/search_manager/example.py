# -*- coding: utf-8 -*-

import os
import random

from visigoth import Diagram
from visigoth.containers import Map
from visigoth.utils.mapping import Projections, Geocoder, Mapping
from visigoth.map_layers import WMS, Geoplot
from visigoth.map_layers.geoplot import Multipoint
from visigoth.containers import Popup, Box
from visigoth.common import SearchManager, Text

folder=os.path.split(__file__)[0]

rng = random.Random()
d = Diagram(fill="white")

gc = Geocoder()
center = gc.fetchCenter("Berlin")
bounds = Mapping.computeBoundaries(center,4000)

lon_min = bounds[0][0]
lon_max = bounds[1][0]
lat_min = bounds[0][1]
lat_max = bounds[1][1]

lon_range = lon_max-lon_min
lat_range = lat_max-lat_min

multipoints=[]
for i in range(20):
    popup = Popup(Text("Popup! %d"%(i)),"popup")
    label = "point_%d"%i
    col = rng.choice(["red","purple","orange","green"])
    lon = lon_min+rng.random()*lon_range
    lat = lat_min+rng.random()*lat_range
    multipoints.append(Multipoint([(lon,lat)],label=label,popup=popup,properties={"type":"point"},fill=col))

gp = Geoplot(multipoints=multipoints)

m = Map(768,boundaries=bounds,projection=Projections.EPSG_3857)

wms = WMS("osm")
wms.setInfo("Map")

sm = SearchManager()
d.add(sm)

m.add(wms)
m.add(gp)
d.add(Text("Berlin Stadtmitte"))
d.add(Box(m))
d.connect(sm,"search",m,"search")

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

