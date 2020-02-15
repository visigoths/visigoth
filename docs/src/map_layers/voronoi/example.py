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
from visigoth.map_layers import Voronoi
from visigoth.utils.colour import Colour
from visigoth.utils.mapping import Projections

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    rng = random.Random()
    data = [(rng.random(),rng.random(),Colour.randomColour(),"area(%d)"%(i)) for i in range(200)]

    d = Diagram(fill="white")
    m = Map(512,boundaries=((0.0,0.0),(1.0,1.0)),projection=Projections.ESPG_4326)
    v = Voronoi(data,radius=5)
    m.addLayer(v)
    d.add(Box(m))

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

