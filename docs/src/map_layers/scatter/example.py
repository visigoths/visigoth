# -*- coding: utf-8 -*-

import random

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import Scatter

rng = random.Random()
bounds = ((0,0),(1,1))
data = [(rng.random(),rng.random()) for x in range(0,200)]

d = Diagram()
m1 = Map(512,bounds)
scatter = Scatter(data,lon=0,lat=1)
scatter.getMarkerManager().setMarkerType("pin").setDefaultRadius(10)
scatter.getPalette().setDefaultColour("blue")
m1.add(scatter)
d.add(Box(m1))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

