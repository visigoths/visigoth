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
import math
import random

from visigoth import Diagram
from visigoth.containers import Box, Map
from visigoth.common import Legend
from visigoth.map_layers import Network
from visigoth.map_layers.network import Node,Edge,DDPageRank
from visigoth.utils.colour import ContinuousPalette

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    d = Diagram(fill="white")

    m1 = Map(512,width_to_height=1)

    nodes = []
    edges = []
    angle = 0
    for i in range(0,10):
        angle = i * math.pi*2 / 10
        lon = 0.5+0.4*math.sin(angle)
        lat = 0.5+0.4*math.cos(angle)

        wlon = 0.5+0.3*math.sin(angle-math.pi/10)
        wlat = 0.5+0.3*math.cos(angle-math.pi/10)
        
        nodes.append(Node(lon,lat,radius=15,fill=random.choice(["red","green","blue"])))
        if len(nodes)>1:
            edges.append(Edge(nodes[-2],nodes[-1],waypoints=[(wlon,wlat)]))

    edges.append(Edge(nodes[-1],nodes[0]))
    edges.append(Edge(nodes[-1],nodes[5]))
    edges.append(Edge(nodes[0],nodes[4]))

    palette = ContinuousPalette()
    palette.addColour("green",0.0)
    palette.addColour("red",1.0)

    nw = Network(nodes=nodes,edges=edges,palette=palette,ranking_algorithm=DDPageRank())
    m1.addLayer(nw)
    d.add(Box(m1))

    d.add(Legend(palette,512))

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

