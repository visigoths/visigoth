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

from visigoth.diagram import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import WMS, GPS
from visigoth.utils.mapping import Projections
from visigoth.common import Text

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    parser.add_argument("--iterations", help="number of iterations to run", default=200,type=int)

    args = parser.parse_args()

    d = Diagram(fill="white")

    bounds  = ((-180,-70),(180,70))
    m = Map(512,bounds,projection=Projections.ESPG_3857,zoom_to=3)
    g = GPS()
    m.addLayer(WMS())
    m.addLayer(g)
    d.add(Box(Text("GPS Test",text_attributes={"font-style":"italic"})))
    d.add(Box(m))
    
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

