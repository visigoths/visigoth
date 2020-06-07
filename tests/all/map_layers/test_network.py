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
from visigoth.common.legend import Legend
from visigoth.utils.colour import ContinuousPalette
from visigoth.utils.marker import MarkerManager
from visigoth.map_layers.network import Network,DDPageRank

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
                for (_,elon,elat) in nodes:
                    dist = math.sqrt((elon-lon)**2+(elat-lat)**2)
                    if dist < 0.1:
                        ok = False
                        break
                if ok:
                    nodes.append((str(i),lon,lat))
                    break
        dists = []
        for (id1,lon1,lat1) in nodes:
            for (id2,lon2,lat2) in nodes:
                if id1 != id2:
                    dist = math.sqrt((lon1-lon2)**2 + (lat1-lat2)**2)
                    dists.append((id1,id2,dist))

        dists = sorted(dists,key=lambda x:x[2])
                    
        for (n1,n2,_) in dists[:100]:
            edges.append((n1,n2))
    
        palette = ContinuousPalette()

        mm = MarkerManager()
        mm.setDefaultRadius(15)

        nw = Network(node_data=nodes,edge_data=edges,palette=palette,marker_manager=mm,ranking_algorithm=DDPageRank())
        m1.addLayer(nw)
        d.add(Box(m1))

        d.add(Legend(palette,512))

        svg = d.draw()
        TestUtils.output(svg,"test_network.svg")

if __name__ == "__main__":
    unittest.main()
