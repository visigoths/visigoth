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
from visigoth.containers import Box, Map
from visigoth.common import Legend
from visigoth.map_layers import Network, WMS
from visigoth.map_layers.network import DDPageRank
from visigoth.utils.colour import ContinuousPalette
from visigoth.utils.marker import MarkerManager

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    d = Diagram(fill="white")

    m1 = Map(512,width_to_height=1)

    nodes = [('0', -0.463, 40.588), ('1', -0.769, 40.170),
     ('2', -0.535, 40.538), ('3', -0.613, 40.026),
     ('4', -0.868, 40.759), ('5', -0.408, 40.343),
     ('6', -0.402, 40.755), ('7', -0.197, 40.580),
     ('8', -0.257, 40.688), ('9', -0.381, 40.518)]

    edges = [
        ('2', '0'), ('1', '3'), ('7', '8'), ('4', '2'), ('7', '9'), ('8', '7'), ('6', '8'), ('4', '0'), ('0', '2'),
     ('8', '6'), ('3', '1'), ('0', '9'), ('5', '9'), ('1', '5'), ('9', '0'), ('5', '2'), ('1', '2'), ('8', '9'),
     ('4', '6'), ('6', '0')]

    palette = ContinuousPalette()
    mm = MarkerManager().setDefaultRadius(10)
    # palette.addColour("green",0.0)
    # palette.addColour("red",1.0)

    nw = Network(node_data=nodes,edge_data=edges,marker_manager=mm,palette=palette,ranking_algorithm=DDPageRank())
    m1.addLayer(WMS("osm").setOpacity(0.5))
    m1.addLayer(nw)
    d.add(Box(m1))


    d.add(Legend(palette,512))

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

