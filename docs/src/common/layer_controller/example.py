# -*- coding: utf-8 -*-

import os

from visigoth import Diagram
from visigoth.containers import Map
from visigoth.utils.mapping import Geocoder, Mapping, Projections
from visigoth.map_layers import WMS
from visigoth.containers import Box
from visigoth.common import Text, LayerController

folder=os.path.split(__file__)[0]

d = Diagram(fill="white")
gc = Geocoder()
center = gc.fetchCenter("Berlin")
bounds = Mapping.computeBoundaries(center,4000)
m = Map(768,boundaries=bounds,projection=Projections.EPSG_3857)

wms1 = WMS("osm")
wms1.setInfo("Open Street Map").setOpacity(0.5)

wms2 = WMS("satellite")
wms2.setInfo("Satellite").setOpacity(0.5)

mlm = LayerController([{"layer":wms1,"label":"Satellite"},{"layer":wms2,"label":"Open Street Map"}],
                      title="Controls",height=150)
d.add(mlm)

m.add(wms1)
m.add(wms2)
d.add(Text("Berlin Stadtmitte"))
d.add(Box(m))
d.connect(mlm,"manage_layers",m,"manage_layers")

html = d.draw(format="html")
f = open("example.html", "w")
f.write(html)
f.close()

