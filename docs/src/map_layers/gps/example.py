# -*- coding: utf-8 -*-

from visigoth.diagram import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import WMS, GPS
from visigoth.utils.mapping import Projections
from visigoth.common import Text

d = Diagram()

bounds  = ((-180,-70),(180,70))
m = Map(512,bounds,projection=Projections.ESPG_3857,zoom_to=4)
g = GPS()
m.addLayer(WMS())
m.addLayer(g)
d.add(Box(Text("GPS Test",text_attributes={"font-style":"italic"})))
d.add(Box(m))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

