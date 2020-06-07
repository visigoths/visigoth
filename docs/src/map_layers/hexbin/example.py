# -*- coding: utf-8 -*-

import random

from visigoth import Diagram
from visigoth.containers import Box, Map
from visigoth.map_layers import Hexbin, Scatter
from visigoth.utils.colour import ContinuousPalette

d = Diagram(fill="white")

rng = random.Random()
bounds = ((0,0),(1,1))
data = [(rng.random(),rng.random()) for x in range(0,100)]

palette = ContinuousPalette()

m1 = Map(512,bounds)
m1.addLayer(Hexbin(data,palette=palette,stroke=None))
m1.addLayer(Scatter(data))
d.add(Box(m1,padding=0))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

