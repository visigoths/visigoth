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
from visigoth.utils.colour import ContinuousColourManager
from visigoth.containers.map import Map
from visigoth.common.legend import Legend
from visigoth.map_layers.hexbin import Hexbin
from visigoth.map_layers.scatter import Scatter

class TestHexbin(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")


        m1 = Map(512)
        rng = random.Random(1)

        data1 = [(rng.random(), rng.random()) for x in range(0, 100)]

        colour_manager1 = ContinuousColourManager()

        m1.add(Hexbin(data1, nr_bins_across=10, colour_manager=colour_manager1,stroke="purple",stroke_width=3))
        m1.add(Scatter(data1))
        legend1 = Legend(colour_manager1,512)
        d.add(m1)
        d.add(legend1)

        m2 = Map(512)
        rng = random.Random(1)

        angles = [math.pi * rng.random() * 2 for r in range(50)]
        data2 = [(0.5+0.2*math.sin(a), 0.5+0.2*math.cos(a)) for a in angles]

        colour_manager2 = ContinuousColourManager()

        m2.add(Hexbin(data2, nr_bins_across=15, colour_manager=colour_manager2,stroke=None))
        m2.add(Scatter(data2))
        legend2 = Legend(colour_manager2, 512)
        d.add(m2)
        d.add(legend2)

        TestUtils.draw_output(d,"test_hexbin")

if __name__ == "__main__":
    unittest.main()
