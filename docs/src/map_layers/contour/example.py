# -*- coding: utf-8 -*-

import argparse
import math

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import Contour
from visigoth.utils.mapping import Projections

d = Diagram()

peaks = [(0.3,0.3,100),(0.1,0.9,150),(0.6,0.7,120)]

def computeHeight(x,y):
    h = 0
    for (cx,cy,height) in peaks:
        d = math.sqrt((x-cx)**2+(y-cy)**2)
        h += height*math.exp(-3*d)
    return h

data = []
resolution=100
for y in range(resolution):
    data.append([computeHeight(x/resolution,y/resolution) for x in range(resolution)])

m = Map(512,boundaries=((20.0,20.0),(21.0,21.0)),projection=Projections.EPSG_3857)
c = Contour(data,10,stroke_width=0.5)
m.addLayer(c)
d.add(Box(m))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

