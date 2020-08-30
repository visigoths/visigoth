# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import WMS
from visigoth.common import Text

d = Diagram()

bounds = ((166.509144322, -46.641235447),(178.517093541, -34.4506617165))

d.add(Text("openstreetmap layer"))
m1 = Map(512,bounds,zoom_to=4)
m1.add(WMS("osm"))
d.add(Box(m1))

d.add(Text("satellite layer"))
m2 = Map(512,bounds,zoom_to=4)
m2.add(WMS("satellite"))
d.add(Box(m2))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

