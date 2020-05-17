# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.containers import Map
from visigoth.map_layers import WMS, Ruler
from visigoth.containers.box import Box

d = Diagram(fill="white")

bounds = ((166.509144322, -46.641235447),(178.517093541, -34.4506617165))

m = Map(512,bounds,zoom_to=2)
m.addLayer(WMS())
m.addLayer(Ruler())
d.add(Box(m))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

