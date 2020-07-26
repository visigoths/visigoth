# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#   and associated documentation files (the "Software"), to deal in the Software without 
#   restriction, including without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or 
#   substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
        m1.add(nw)
        d.add(Box(m1))

        d.add(Legend(palette,512))

        TestUtils.draw_output(d,"test_network")

if __name__ == "__main__":
    unittest.main()
