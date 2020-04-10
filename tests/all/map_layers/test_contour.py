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
        m0.addLayer(c0)
        d.add(Box(m0))

        peaks1 = [(0.3, 0.3, 100), (0.1, 0.9, 150), (0.6, 0.7, 120)]

        resolution1 = 100
        data1 = [[self.computeHeight(peaks1, x/resolution1, y/resolution1) for x in range(resolution1)] for y in range(resolution1)]

        m1 = Map(512, projection=Projections.IDENTITY)
        c1 = Contour(data1, 10, stroke_width=0.5)
        m1.addLayer(c1)
        d.add(Box(m1))

        peaks2 = [(x/10,y/10,10) for x in [2,6] for y in [3,9]]

        resolution2 = 100
        data2 = [[self.computeHeight(peaks2, x / resolution2, y / resolution2) for x in range(resolution2*2)] for y in
                 range(resolution2)]

        m2 = Map(512, projection=Projections.IDENTITY)
        c2 = Contour(data2, 1, stroke_width=2, stroke="blue")
        m2.addLayer(c2)
        d.add(Box(m2))



        svg = d.draw()
        TestUtils.output(svg,"test_contour.svg")

    def test_edge(self):
        d = Diagram(fill="white")

        m1 = Map(512, boundaries=((0, 0), (1, 1)), projection=Projections.IDENTITY)
        c1 = Contour() # empty contour plot?
        m1.addLayer(c1)
        d.add(Box(m1))

        data2 = [[1, 0, 0, 0, 1], [0, 0, 1, 0, 0], [0, 1, 2.5, 1, 0], [0, 0, 1, 0, 0], [1, 0, 0, 0, 1]]

        m2 = Map(512, boundaries=((0, 0), (1, 1)), projection=Projections.IDENTITY)
        c2 = Contour(data2, 1, stroke_width=0.5)
        m2.addLayer(c2)
        d.add(Box(m2))

        svg = d.draw()
        TestUtils.output(svg, "test_contour_edge.svg")

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
