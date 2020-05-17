# -*- coding: utf-8 -*-

import random

from visigoth.diagram import Diagram
from visigoth.containers import Box, Map, Popup
from visigoth.map_layers import Geoplot, WMS
from visigoth.common import Text
from visigoth.map_layers.geoplot import Multipoint,Multiline,Multipolygon
from visigoth.utils.mapping import Geocoder,Projections

rng = random.Random()
d = Diagram()

gc = Geocoder()
bb = gc.fetchBoundingBox("Berlin")

lon_min = bb[0][0]
lon_max = bb[1][0]
lat_min = bb[0][1]
lat_max = bb[1][1]

lon_range = lon_max-lon_min
lat_range = lat_max-lat_min

multipoints=[]
for i in range(20):
    popup = Popup(Text("Popup! %d"%(i)),"popup")
    label = "point_%d"%i
    col = rng.choice(["red","purple","orange","green"])
    lon = lon_min+rng.random()*lon_range
    lat = lat_min+rng.random()*lat_range
    multipoints.append(Multipoint([(lon,lat)],id=label,label=label,popup=popup,properties={"type":"point"},fill=col))

multilines=[]
popup = Popup(Text("Popup! %d"%(i)),"popup")
label = "line_%d"%i
multiline = []
multiline.append((lon_min+lon_range*0.1,lat_min+lat_range*0.2))
multiline.append((lon_min+lon_range*0.3,lat_min+lat_range*0.3))
multiline.append((lon_min+lon_range*0.5,lat_min+lat_range*0.6))
multiline.append((lon_min+lon_range*0.8,lat_min+lat_range*0.9))
multilines.append(Multiline([multiline],id=label,label=label,popup=popup,properties={"type":"line"},fill="white",width=10,stroke="red",stroke_width=3))

multipolys=[]

lps = []

lps.append((lon_min+lon_range*0.6,lat_min+lat_range*0.5))
lps.append((lon_min+lon_range*0.9,lat_min+lat_range*0.5))
lps.append((lon_min+lon_range*0.9,lat_min+lat_range*0.8))
lps.append((lon_min+lon_range*0.6,lat_min+lat_range*0.8))

hole = []

hole.append((lon_min+lon_range*0.7,lat_min+lat_range*0.6))
hole.append((lon_min+lon_range*0.8,lat_min+lat_range*0.6))
hole.append((lon_min+lon_range*0.8,lat_min+lat_range*0.7))
hole.append((lon_min+lon_range*0.7,lat_min+lat_range*0.7))

popup = Popup(Text("Popup! %d"%(i)),"popup")
label = "poly_%d"%i
multipolys.append(Multipolygon([[lps,hole]],id=label,label=label,popup=popup,properties={"type":"poly"},stroke="red",fill="#0000FF30"))

m = Map(512,boundaries=bb,projection=Projections.ESPG_3857,zoom_to=2)
m.addLayer(WMS())
gp = Geoplot(multipoints=multipoints,multilines=multilines,multipolys=multipolys)
m.addLayer(gp)

gj = Box(m)
d.add(gj)
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

