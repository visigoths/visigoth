# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import argparse
import math
import random

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import Cluster
from visigoth.map_layers.cluster import AgglomerativeAlgorithm

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

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
    m1.addLayer(Cluster(data,algorithm=alg))
    d.add(Box(m1))

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

