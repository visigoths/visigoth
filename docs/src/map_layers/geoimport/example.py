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

import os.path
import argparse
import random

from visigoth.diagram import Diagram
from visigoth.map_layers import Geoimport
from visigoth.containers import Map

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    rng = random.Random()
    d = Diagram(fill="white")
    m1 = Map(512)

    path = os.path.join(os.path.split(__file__)[0],"nz_region.geojson")

    m1.addLayer(Geoimport(path,polygon_style=lambda p:{"tooltip":p["REGC2016_N"],"fill":rng.choice(["red","orange","yellow"])}))
    d.add(m1)

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

