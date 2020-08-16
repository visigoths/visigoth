# -*- coding: utf-8 -*-

import random
import math

from visigoth.diagram import Diagram
from visigoth.containers import Map, Box
from visigoth.common import Legend
from visigoth.map_layers.cartogram import Cartogram
from visigoth.utils.mapping.projections import Projections
from visigoth.utils.colour import DiscretePalette
from visigoth.utils.marker import MarkerManager

d = Diagram(fill="white")

rng = random.Random(3)
cluster_count = 6

def gen(px,py,maxdist):
    angle = rng.random()*2*math.pi
    d = rng.random()*maxdist
    dx = d*math.sin(angle)
    dy = d*math.cos(angle)
    size = random.choice([2,3,4])
    cat = random.choice(["cat1", "cat2", "cat3"])
    label = "cat: "+cat
    return (px+dx,py+dy,cat,label,size)

palette = DiscretePalette()
mm = MarkerManager(max_radius=20)

cluster_centers = [(0.05+0.9*rng.random(),0.05+0.9*rng.random()) for x in range(0,cluster_count)]
data = [gen(cx,cy,0.1) for (cx,cy) in cluster_centers for x in range(0,10)]

bounds  = ((0.0,0.0),(1.0,1.0))
m = Map(512,bounds,projection=Projections.IDENTITY)
c = Cartogram(data, palette=palette, marker_manager=mm, lon=0, lat=1, colour=2, label=3, size=4, iterations=300)
m.add(c)
legend = Legend(palette, width=500, legend_columns=3)
d.add(Box(m))
d.add(legend)

d.connect(c,"colour",legend,"colour")
d.connect(legend,"colour",c,"colour")

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

