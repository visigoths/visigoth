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

import unittest
import random
import math

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.containers.map import Map
from visigoth.containers.box import Box
from visigoth.common.space import Space
from visigoth.common.legend import Legend
from visigoth.utils.colour import ContinuousPalette
from visigoth.map_layers.network import Network,Node,Edge,DDPageRank

class TestNetwork(unittest.TestCase):

    def test_basic(self):

        d = Diagram(fill="white")

        m1 = Map(512,width_to_height=1)

        nodes = []
        edges = []
        
        for i in range(0,50):
            tries = 0
            while tries < 10:
                tries += 1
                lon = random.random()
                lat = random.random()
                ok = True
                for existing in nodes:
                    (elon,elat) = existing.getLonLat()
                    dist = math.sqrt((elon-lon)**2+(elat-lat)**2)
                    if dist < 0.1:
                        ok = False
                        break
                if ok:
                    nodes.append(Node(lon,lat,radius=15,fill=random.choice(["red","green","blue"])))
                    break
        dists = []
        for n1 in nodes:
            for n2 in nodes:
                if n2 != n1:
                    (lon1,lat1) = n1.getLonLat()
                    (lon2,lat2) = n2.getLonLat()
                    dist = math.sqrt((lon1-lon2)**2 + (lat1-lat2)**2)
                    dists.append((n1,n2,dist))

        dists = sorted(dists,key=lambda x:x[2])
                    
        for (n1,n2,_) in dists[:100]:
            edges.append(Edge(n1,n2))
    
        palette = ContinuousPalette()
        palette.addColour("blue",0.0)
        palette.addColour("red",1.0)

        nw = Network(nodes=nodes,edges=edges,palette=palette,ranking_algorithm=DDPageRank())
        m1.addLayer(nw)
        d.add(Box(m1))

        d.add(Legend(palette,512))

        svg = d.draw()
        TestUtils.output(svg,"test_network.svg")

if __name__ == "__main__":
    unittest.main()
