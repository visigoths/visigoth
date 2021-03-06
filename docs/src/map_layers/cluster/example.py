# -*- coding: utf-8 -*-

import math
import random

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import Cluster
from visigoth.map_layers.cluster import AgglomerativeAlgorithm

d = Diagram(fill="white")

rng = random.Random()
bounds = ((0,0),(1,1))
cluster_count = 5

def jitter(px,py,maxdist):
    angle = rng.random()*2*math.pi
    r = rng.random()*maxdist
    dx = r*math.sin(angle)
    dy = r*math.cos(angle)
    return (px+dx,py+dy)

cluster_centers = [(rng.random(),rng.random(),0.1*rng.random()) for x in range(0,cluster_count)]
data = [jitter(cx,cy,cr) for (cx,cy,cr) in cluster_centers for x in range(0,20)]
m1 = Map(512,bounds,zoom_to=4)
# alg = KMeansAlgorithm(cluster_count_min=3,cluster_count_max=8)
alg = AgglomerativeAlgorithm(max_distance=10000)
m1.add(Cluster(data,algorithm=alg))
d.add(Box(m1))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

