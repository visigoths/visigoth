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

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.map_layers.cartogram import Cartogram
from visigoth.containers.map import Map
from visigoth.containers.box import Box
from visigoth.common import Legend, Text
from visigoth.utils.mapping.projections import Projections
from visigoth.utils.colour import DiscreteColourManager

class TestCartogram(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        rng = random.Random(3)

        def gen(cx,cy,minr,maxr):
            radius = minr+rng.random()*(maxr-minr)
            cat = random.choice(["cat1", "cat2", "cat3"])
            label = "cat: "+cat
            return (cx,cy,cat,label,radius)

        colour_manager = DiscreteColourManager()
        colour_manager.addColour("cat1","yellow")
        colour_manager.addColour("cat2","green")
        colour_manager.addColour("cat3","purple")

        for (data_size,scale) in [(25,1),(50,1),(100,0.5)]:
            data = [gen(cx,cy,20*scale,50*scale) for (cx,cy) in [(0.25,0.25),(0.75,0.75),(0.25,0.75),(0.75,0.25)] for _ in range(0,data_size)]

            bounds  = ((0.0,0.0),(1.0,1.0))
            m = Map(512,bounds,projection=Projections.IDENTITY)
            c = Cartogram(data, colour=2, size=4, colour_manager=colour_manager, iterations=500, link_stroke="red")
            m.add(c)
            legend = Legend(colour_manager, width=500, legend_columns=3)
            d.add(Text(str(data_size)))
            d.add(Box(m))
            d.add(legend)

            d.connect(c,"colour",legend,"colour")
            d.connect(legend,"colour",c,"colour")

        TestUtils.draw_output(d,"test_cartogram")

if __name__ == "__main__":
    unittest.main()
