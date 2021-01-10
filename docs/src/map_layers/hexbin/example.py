# -*- coding: utf-8 -*-

import random

from visigoth import Diagram
from visigoth.containers import Box, Map
from visigoth.map_layers import Hexbin, Scatter
from visigoth.utils.colour import ContinuousColourManager

d = Diagram(fill="white")

rng = random.Random()
bounds = ((0,0),(1,1))
data = [(rng.random(),rng.random()) for x in range(0,100)]

colour_manager = ContinuousColourManager(colourMap=["orange","purple"])

m1 = Map(512,bounds)
m1.add(Hexbin(data,colour_manager=colour_manager,stroke=None))
m1.add(Scatter(data))
d.add(Box(m1,padding=0))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

