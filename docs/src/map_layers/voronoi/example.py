# -*- coding: utf-8 -*-

import random

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import Voronoi
from visigoth.utils.mapping import Projections

rng = random.Random()
data = [(rng.random(),rng.random(),i,"area(%d)"%(i)) for i in range(200)]

d = Diagram(fill="white")
m = Map(512,boundaries=((0.0,0.0),(1.0,1.0)),projection=Projections.ESPG_4326)
v = Voronoi(data,lat=0,lon=1,colour=2,label=3)
v.getMarkerManager().setDefaultRadius(5)
m.addLayer(v)
d.add(Box(m))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

