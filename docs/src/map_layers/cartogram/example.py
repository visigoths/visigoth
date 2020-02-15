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
import random
import math

from visigoth.diagram import Diagram
from visigoth.containers import Map, Box
from visigoth.common import Legend
from visigoth.map_layers.cartogram import Cartogram
from visigoth.utils.mapping.projections import Projections
from visigoth.utils.colour import DiscretePalette

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    parser.add_argument("--iterations", help="number of iterations to run", default=200,type=int)

    args = parser.parse_args()

    d = Diagram(fill="white")

    rng = random.Random(3)

    cluster_count = 6

    def gen(px,py,maxdist,minr,maxr):
        angle = rng.random()*2*math.pi
        d = rng.random()*maxdist
        dx = d*math.sin(angle)
        dy = d*math.cos(angle)
        radius = minr+rng.random()*(maxr-minr)
        cat = random.choice(["cat1", "cat2", "cat3"])
        label = "cat: "+cat
        return (px+dx,py+dy,cat,label,radius)

    palette = DiscretePalette()
    palette.addCategory("cat1","red")
    palette.addCategory("cat2","green")
    palette.addCategory("cat3","blue")

    cluster_centers = [(0.05+0.9*rng.random(),0.05+0.9*rng.random()) for x in range(0,cluster_count)]
    data = [gen(cx,cy,0.1,10,25) for (cx,cy) in cluster_centers for x in range(0,10)]

    bounds  = ((0.0,0.0),(1.0,1.0))
    m = Map(512,bounds,projection=Projections.IDENTITY)
    c = Cartogram(data, palette, iterations=args.iterations, stroke_width=0.5)
    m.addLayer(c)
    legend = Legend(palette, width=500, legend_columns=3)
    d.add(Box(m))
    d.add(legend)

    d.connect(c,"brushing",legend,"brushing")
    d.connect(legend,"brushing",c,"brushing")

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

