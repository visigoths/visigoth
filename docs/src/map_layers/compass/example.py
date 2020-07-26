# -*- coding: utf-8 -*-

from visigoth.diagram import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import WMS, Compass
from visigoth.common import Text

d = Diagram()

bounds  = ((-180,-70),(180,70))
m = Map(512,bounds)
m.add(WMS(type="osm"))
m.add(Compass())
d.add(Box(Text("Compass Test",text_attributes={"font-style":"italic"})))
d.add(Box(m))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

