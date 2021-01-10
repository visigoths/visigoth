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
import math

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.containers import Map, Box
from visigoth.map_layers import ColourGrid
from visigoth.utils.colour import ContinuousColourManager
from visigoth.utils.mapping.projections import Projections
from visigoth.common import Legend

class TestColourGrid(unittest.TestCase):

    def computeHeight(self, peaks, x, y):
        h = 0
        for (cx, cy, height) in peaks:
            d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            h += height * math.exp(-3 * d)
        return h

    def test_basic(self):
        d = Diagram(fill="white")

        peaks0 = [(0.75, 0.65, 100)]
        peaks1 = [(0.3, 0.5, 150)]
        peaks2 = [(0.2, 0.8, 120)]

        resolution0 = 300
        data0 = [[self.computeHeight(peaks0, x / resolution0, y / resolution0)+
                  self.computeHeight(peaks1, x / resolution0, y / resolution0)+
                  self.computeHeight(peaks2, x / resolution0, y / resolution0) for x in range(resolution0)] for y in
                 range(resolution0)]

        lons = [(i+0.5)*1/300 for i in range(300)]
        lats = [(i+0.5)*1/300 for i in range(300)]

        m0 = Map(512, projection=Projections.IDENTITY, boundaries=((0.0,0.0),(1.0,1.0)))
        c0 = ColourGrid(data0, lons=lons, lats=lats ,colour_manager=ContinuousColourManager(withIntervals=True))
        m0.add(c0)

        d.add(Box(m0))
        d.add(Legend(width=512, colour_manager=c0.getPalette()))
        #
        # peaks1 = [(0.3, 0.3, 100), (0.1, 0.9, 150), (0.6, 0.7, 120)]
        #
        # resolution1 = 400
        # data1 = [[self.computeHeight(peaks1, x/resolution1, y/resolution1) for x in range(resolution1)] for y in range(resolution1)]
        #
        # m1 = Map(512, projection=Projections.IDENTITY,boundaries=((0.0,0.0),(1.0,1.0)))
        # c1 = ColourGrid(data1,boundaries=((0,0),(1,1)))
        # m1.add(c1)
        # d.add(Box(m1))
        # d.add(Legend(width=512, colour_manager=c1.getPalette()))
        #
        # peaks2 = [(x/10,y/10,10) for x in [2,6] for y in [3,9]]
        #
        # resolution2 = 500
        # data2 = [[self.computeHeight(peaks2, x / resolution2, y / resolution2) for x in range(resolution2*2)] for y in
        #          range(resolution2)]
        #
        # m2 = Map(512, projection=Projections.IDENTITY,boundaries=((0.0,0.0),(1.0,1.0)))
        # c2 = ColourGrid(data2, boundaries=((0,0),(1,1)))
        # m2.add(c2)
        # d.add(Box(m2))
        # d.add(Legend(width=512, colour_manager=c2.getPalette()))

        TestUtils.draw_output(d,"test_colourgrid")


if __name__ == "__main__":
    unittest.main()
