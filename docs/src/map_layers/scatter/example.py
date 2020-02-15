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

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import Scatter

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    d = Diagram(fill="white")

    rng = random.Random()
    bounds = ((0,0),(1,1))
    data = [(rng.random(),rng.random()) for x in range(0,200)]

    m1 = Map(512,bounds)
    m1.addLayer(Scatter(data,fill="green"))
    d.add(Box(m1))

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

