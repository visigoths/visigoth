# -*- coding: utf-8 -*-

import os.path
import random

from visigoth.diagram import Diagram
from visigoth.map_layers import Geoimport
from visigoth.containers import Map

rng = random.Random()
d = Diagram(fill="white")
m1 = Map(512)

path = os.path.join(os.path.split(__file__)[0],"nz_region.geojson")

m1.addLayer(Geoimport(path,polygon_style=lambda p:{"tooltip":p["REGC2016_N"],"fill":rng.choice(["red","orange","yellow"])}))
d.add(m1)

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

