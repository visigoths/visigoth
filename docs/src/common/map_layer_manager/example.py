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

import os
import argparse

from visigoth import Diagram

from visigoth.containers.map import Map
from visigoth.utils.mapping import Geocoder, Mapping

from visigoth.map_layers import GridSquares, WMS
from visigoth.containers import Box
from visigoth.common import Text, MapLayerManager

from visigoth.utils.mapping import Projections

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    folder=os.path.split(__file__)[0]

    d = Diagram(fill="white")

    gc = Geocoder()
    center = gc.fetchCenter("Berlin")
    bounds = Mapping.computeBoundaries(center,4000)
    m = Map(768,boundaries=bounds,projection=Projections.ESPG_3857)

    wms = WMS("osm")
    wms.setInfo("Map")

    grid = GridSquares()
    grid.setOpacity(0.8)
    grid.setVisible(False)

    mlm = MapLayerManager([{"layer":grid,"label":"Grid"},{"layer":wms,"label":"Satellite"}],title="< Controls >",height=150)
    d.add(mlm)

    m.addLayer(wms)
    m.addLayer(grid)
    d.add(Text("Berlin Stadtmitte"))
    d.add(Box(m))
    d.connect(mlm,"manage_layers",m,"manage_layers")

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

