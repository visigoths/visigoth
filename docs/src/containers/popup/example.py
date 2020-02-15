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

from visigoth.containers import Map, Popup
from visigoth.utils.mapping import Geocoder
from visigoth.map_layers import GridSquares, WMS, Geoplot
from visigoth.map_layers.geoplot import Multipoint
from visigoth.common import Space
from visigoth.utils.mapping import Mapping, Projections

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    folder=os.path.split(__file__)[0]

    d = Diagram(fill="white")

    gc = Geocoder()

    center = gc.fetchCenter("New York")
    bounds = Mapping.computeBoundaries(center,200000,projection=Projections.ESPG_3857)

    timesq = gc.fetchCenter("Times Square, New York")
    timesq_bounds = Mapping.computeBoundaries(timesq,500,projection=Projections.ESPG_3857)
    

    timesq_m = Map(256,boundaries=timesq_bounds,projection=Projections.ESPG_3857,font_height=5)
    timesq_wms = WMS(type="osm")
    timesq_m.addLayer(timesq_wms)
    timesq_popup = Popup(timesq_m,"Times Square",fill="white")

    m = Map(512,boundaries=bounds,projection=Projections.ESPG_3857,zoom_to=2)

    wms = WMS(type="osm")
    wms.setInfo("Map")

    gp = Geoplot(multipoints=[Multipoint([timesq],label="Times Square",popup=timesq_popup)])
    grid = GridSquares()

    m.addLayer(wms)
    m.addLayer(gp)
    m.addLayer(grid)
    d.add(Space(100))
    d.add(m)

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()



