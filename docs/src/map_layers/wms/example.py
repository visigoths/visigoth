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

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import WMS
from visigoth.common import Text

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    d = Diagram(fill="white")

    bounds = ((166.509144322, -46.641235447),(178.517093541, -34.4506617165))

    d.add(Text("openstreetmap layer"))
    m1 = Map(512,bounds,zoom_to=4)
    m1.addLayer(WMS("osm"))
    d.add(Box(m1))

    d.add(Text("sentinel2 cloudless layer"))
    m2 = Map(512,bounds,zoom_to=4)
    m2.addLayer(WMS("satellite"))
    d.add(Box(m2))

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

