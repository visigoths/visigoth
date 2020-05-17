# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.common import PanZoom

d = Diagram()
pz = PanZoom(4)
d.add(pz)

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()
