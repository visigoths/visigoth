# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import argparse
import random

from visigoth import Diagram

from visigoth.containers.map import Map
from visigoth.utils.mapping import Metadata, Geocoder, Mapping


from visigoth.map_layers import WMS, Geoplot, GridSquares
from visigoth.map_layers.geoplot import Multipoint
from visigoth.containers.popup import Popup
from visigoth.containers.box import Box
from visigoth.common.text import Text
from visigoth.common import SearchManager

from visigoth.utils.mapping import Projections

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    folder=os.path.split(__file__)[0]

    rng = random.Random()
    d = Diagram(fill="white")

    gc = Geocoder()
    center = gc.fetchCenter("Berlin")
    bounds = Mapping.computeBoundaries(center,4000)

    lon_min = bounds[0][0]
    lon_max = bounds[1][0]
    lat_min = bounds[0][1]
    lat_max = bounds[1][1]

    lon_range = lon_max-lon_min
    lat_range = lat_max-lat_min

    multipoints=[]
    for i in range(20):
        popup = Popup(Text("Popup! %d"%(i)),"popup")
        label = "point_%d"%i
        col = rng.choice(["red","purple","orange","green"])
        lon = lon_min+rng.random()*lon_range
        lat = lat_min+rng.random()*lat_range
        multipoints.append(Multipoint([(lon,lat)],label=label,popup=popup,properties={"type":"point"},fill=col))

    gp = Geoplot(multipoints=multipoints)

    m = Map(768,boundaries=bounds,projection=Projections.ESPG_3857)

    wms = WMS("osm")
    wms.setInfo("Map")

    grid = GridSquares()
    grid.setOpacity(0.8)
    grid.setVisible(False)

    sm = SearchManager(height=150)
    d.add(sm)

    m.addLayer(wms)
    m.addLayer(grid)
    m.addLayer(gp)
    d.add(Text("Berlin Stadtmitte"))
    d.add(Box(m))
    d.connect(sm,"search",m,"search")

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()
