# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.utils.mapping import Projections, Geocoder, Mapping
from visigoth.map_layers import Scatter, WMS
from visigoth.common import Text

d = Diagram()

gc = Geocoder()
center = gc.fetchCenter("Berlin")
bounds = Mapping.computeBoundaries(center,10000,projection=Projections.ESPG_3857)

m = Map(400,boundaries=bounds,zoom_to=5,projection=Projections.ESPG_3857)

s = Scatter([center])
s.getMarkerManager().setDefaultRadius(20).setMarkerType("pin")
s.getPalette().setDefaultColour("darkred")
wms = WMS(type="osm")
wms.setInfo("Map")

m.addLayer(wms)
m.addLayer(s)
d.add(Text("Berlin Stadtmitte"))
d.add(Box(m))

html = d.draw(format="html")
f = open("example.html", "w")
f.write(html)
f.close()

