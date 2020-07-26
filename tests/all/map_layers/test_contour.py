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
from visigoth.containers.map import Map
from visigoth.containers.box import Box
from visigoth.map_layers.contour import Contour
from visigoth.utils.mapping.projections import Projections

class TestContour(unittest.TestCase):

    def computeHeight(self, peaks, x, y):
        h = 0
        for (cx, cy, height) in peaks:
            d = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
            h += height * math.exp(-3 * d)
        return h

    def test_basic(self):
        d = Diagram(fill="white")

        peaks0 = [(0.5, 0.5, 100)]

        resolution0 = 50
        data0 = [[self.computeHeight(peaks0, x / resolution0, y / resolution0) for x in range(resolution0)] for y in
                 range(resolution0)]

        m0 = Map(512, projection=Projections.IDENTITY)
        c0 = Contour(data0, 5, stroke_width=0.5)
        m0.add(c0)
        d.add(Box(m0))

        peaks1 = [(0.3, 0.3, 100), (0.1, 0.9, 150), (0.6, 0.7, 120)]

        resolution1 = 100
        data1 = [[self.computeHeight(peaks1, x/resolution1, y/resolution1) for x in range(resolution1)] for y in range(resolution1)]

        m1 = Map(512, projection=Projections.IDENTITY)
        c1 = Contour(data1, 10, stroke_width=0.5)
        m1.add(c1)
        d.add(Box(m1))

        peaks2 = [(x/10,y/10,10) for x in [2,6] for y in [3,9]]

        resolution2 = 100
        data2 = [[self.computeHeight(peaks2, x / resolution2, y / resolution2) for x in range(resolution2*2)] for y in
                 range(resolution2)]

        m2 = Map(512, projection=Projections.IDENTITY)
        c2 = Contour(data2, 1, stroke_width=2, stroke="blue")
        m2.add(c2)
        d.add(Box(m2))

        TestUtils.draw_output(d,"test_contour")

    def test_edge(self):
        d = Diagram(fill="white")

        m1 = Map(512, boundaries=((0, 0), (1, 1)), projection=Projections.IDENTITY)
        c1 = Contour() # empty contour plot?
        m1.add(c1)
        d.add(Box(m1))

        data2 = [[1, 0, 0, 0, 1], [0, 0, 1, 0, 0], [0, 1, 2.5, 1, 0], [0, 0, 1, 0, 0], [1, 0, 0, 0, 1]]

        m2 = Map(512, boundaries=((0, 0), (1, 1)), projection=Projections.IDENTITY)
        c2 = Contour(data2, 1, stroke_width=0.5)
        m2.add(c2)
        d.add(Box(m2))

        TestUtils.draw_output(d, "test_contour_edge")

    def test_negative(self):
        try:
            c = Contour([[]],1)
            self.assertFalse(True)
        except Exception as ex:
            self.assertEqual(ex.args[0],Contour.INPUT_DATA_FORMAT_ERROR)

        try:
            c = Contour([[1,2,3],[4,5]],1)
            self.assertFalse(True)
        except Exception as ex:
            self.assertEqual(ex.args[0],Contour.INPUT_DATA_FORMAT_ERROR)

        try:
            c = Contour(contour_interval=-1)
            self.assertFalse(True)
        except Exception as ex:
            self.assertEqual(ex.args[0],Contour.CONTOUR_INTERVAL_ERROR)


if __name__ == "__main__":
    unittest.main()
