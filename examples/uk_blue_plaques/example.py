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

from visigoth.diagram import Diagram
from visigoth.map_layers import Geoimport,WMS
from visigoth.common.text import Text
from visigoth.common.space import Space
from visigoth.containers.map import Map
from visigoth.utils.mapping import Projections
from visigoth.utils.httpcache import HttpCache

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    rng = random.Random()
    d = Diagram(fill="white")

    projection=Projections.ESPG_3857
    bounds = ((-10.8544921875,49.82380908513249),
              (2.021484375,59.478568831926395))

    m1 = Map(768,bounds,projection,zoom_to=4)

    path = HttpCache.fetch("https://s3.eu-west-2.amazonaws.com/openplaques/open-plaques-United-Kingdom-2018-04-08.geojson",suffix=".geojson",returnPath=True)

    plaques = Geoimport(path,point_style=lambda p:{"fill":"lightblue","marker":False,"radius":3,"tooltip":p["inscription"]})
    plaques.setInfo("Blue Plaques","",attribution="http://openplaques.org/pages/data",url="http://openplaques.org/pages/data")

    m1.addLayer(WMS())
    m1.addLayer(plaques)
    d.add(m1)
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

