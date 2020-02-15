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

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import Contour
from visigoth.utils.mapping import Projections

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    d = Diagram(fill="white")

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

    m = Map(512,boundaries=((20.0,20.0),(21.0,21.0)),projection=Projections.ESPG_3857)
    c = Contour(data,10,stroke_width=0.5)
    m.addLayer(c)
    d.add(Box(m))

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

