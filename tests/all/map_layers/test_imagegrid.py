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
from visigoth.map_layers import ImageGrid
from visigoth.utils.mapping.projections import Projections
from visigoth.common import Legend

class TestImageGrid(unittest.TestCase):

    def computeHeight(self, peaks, x, y):
        h = 0
        for (cx, cy, height) in peaks:
            d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            h += height * math.exp(-3 * d)
        return int(h)

    def test_basic(self):
        d = Diagram(fill="white")

        red_peaks = [(0.75, 0.65, 100)]
        green_peaks = [(0.3, 0.5, 150)]
        blue_peaks = [(0.2, 0.8, 120)]

        resolution0 = 300
        red_data = [[self.computeHeight(red_peaks, x / resolution0, y / resolution0)
                     for x in range(resolution0)] for y in range(resolution0)]
        green_data = [[self.computeHeight(green_peaks, x / resolution0, y / resolution0)
                     for x in range(resolution0)] for y in range(resolution0)]
        blue_data = [[self.computeHeight(blue_peaks, x / resolution0, y / resolution0)
                      for x in range(resolution0)] for y in range(resolution0)]

        lons = [(i+0.5)*1/300 for i in range(300)]
        lats = [(i+0.5)*1/300 for i in range(300)]

        m0 = Map(512, projection=Projections.IDENTITY, boundaries=((0.0,0.0),(1.0,1.0)))
        c0 = ImageGrid(r=red_data,g=green_data,b=blue_data,a=None,lons=lons, lats=lats)
        m0.add(c0)

        d.add(Box(m0))

        TestUtils.draw_output(d,"test_imagegrid")


if __name__ == "__main__":
    unittest.main()
