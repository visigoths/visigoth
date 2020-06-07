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
from visigoth.containers import Map, Box
from visigoth.map_layers import ColourGrid
from visigoth.utils.colour import ContinuousPalette
from visigoth.utils.mapping.projections import Projections
from visigoth.common import Legend

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

        resolution0 = 300
        data0 = [[self.computeHeight(peaks0, x / resolution0, y / resolution0) for x in range(resolution0)] for y in
                 range(resolution0)]

        m0 = Map(512, projection=Projections.IDENTITY, boundaries=((0.0,0.0),(1.0,1.0)))
        c0 = ColourGrid(data0, boundaries=((0.0,0.0),(1.0,1.0)),palette=ContinuousPalette(withIntervals=True))
        m0.addLayer(c0)

        d.add(Box(m0))
        d.add(Legend(width=512, palette=c0.getPalette()))

        peaks1 = [(0.3, 0.3, 100), (0.1, 0.9, 150), (0.6, 0.7, 120)]

        resolution1 = 400
        data1 = [[self.computeHeight(peaks1, x/resolution1, y/resolution1) for x in range(resolution1)] for y in range(resolution1)]

        m1 = Map(512, projection=Projections.IDENTITY,boundaries=((0.0,0.0),(1.0,1.0)))
        c1 = ColourGrid(data1,boundaries=((0,0),(1,1)))
        m1.addLayer(c1)
        d.add(Box(m1))
        d.add(Legend(width=512, palette=c1.getPalette()))

        peaks2 = [(x/10,y/10,10) for x in [2,6] for y in [3,9]]

        resolution2 = 500
        data2 = [[self.computeHeight(peaks2, x / resolution2, y / resolution2) for x in range(resolution2*2)] for y in
                 range(resolution2)]

        m2 = Map(512, projection=Projections.IDENTITY,boundaries=((0.0,0.0),(1.0,1.0)))
        c2 = ColourGrid(data2, boundaries=((0,0),(1,1)))
        m2.addLayer(c2)
        d.add(Box(m2))
        d.add(Legend(width=512, palette=c2.getPalette()))

        svg = d.draw()
        TestUtils.output(svg,"test_colourgrid.svg")


if __name__ == "__main__":
    unittest.main()
