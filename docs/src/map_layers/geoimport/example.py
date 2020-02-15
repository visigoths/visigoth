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
from visigoth.common import Text, Space
from visigoth.containers import Map
from visigoth.utils.mapping import Projections
from visigoth.utils.httpcache import HttpCache

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    rng = random.Random()
    d = Diagram(fill="white")

    projection=Projections.ESPG_3857
    bounds = None
    m1 = Map(1024,bounds,projection)

    d.add(Text("GeoPackage Example",font_height=50,text_attributes={"stroke":"purple"}))
    d.add(Space(20,20))

    path = "/tmp/rivers.gpkg"

    if not os.path.exists(path):
        url = "https://raw.githubusercontent.com/opengeospatial/ets-gpkg12/master/src/test/resources/gpkg/rivers.gpkg"
        with open(path,"wb") as f:
            f.write(HttpCache.fetch(url))

    m1.addLayer(Geoimport(path,line_style=lambda p:{"stroke":rng.choice(["red","green","blue"])}))
    d.add(m1)
    d.add(Text("Attribution: https://github.com/opengeospatial/ets-gpkg12",url="https://github.com/opengeospatial/ets-gpkg12",font_height=18))

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

