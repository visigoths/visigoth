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
from visigoth.map_layers.voronoi import Voronoi
from visigoth.utils.colour import DiscreteColourManager
from visigoth.utils.marker import MarkerManager

class TestVoronoi(unittest.TestCase):

    def test_basic(self):
        d = Diagram()

        m1 = Map(512)
        rng = random.Random(1)

        data1 = [(rng.random(), rng.random(), str(x), "p"+str(x)) for x in range(0, 100)]
        p = DiscreteColourManager()
        mm = MarkerManager()
        mm.setDefaultRadius(5)
        m1.add(Voronoi(data1,colour_manager=p,lon=0,lat=1,colour=2,marker_manager=mm))
        d.add(Box(m1))

        m2 = Map(512)
        rng = random.Random(1)

        angles2 = [math.pi * rng.random() * 2 for r in range(15)]

        data2 = [(0.5 + (0.4+0.1*rng.random())*math.sin(a), 0.5 + (0.4 + 0.1*rng.random())*math.cos(a)) for a in angles2]
        data2v = [(x,y,random.choice(["A","B","C"])) for (x,y) in data2]

        m2.add(Voronoi(data2v,lon=0,lat=1,colour=2,label=2))

        d.add(Box(m2))

        TestUtils.draw_output(d,"test_voronoi")

    def test_square(self):
        d = Diagram()

        m1 = Map(512)

        p = DiscreteColourManager()
        p.addColour("A","red").addColour("B","blue").addColour("C","green").addColour("D","orange")

        data1 = [(0.25,0.25,"A"),
                 (0.75,0.75,"B"),
                 (0.25,0.75,"C"),
                 (0.75,0.25,"D")]

        m1.add(Voronoi(data1))
        d.add(Box(m1))

        TestUtils.draw_output(d,"test_voronoi_square")


if __name__ == "__main__":
    unittest.main()
