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
from visigoth.containers.box import Box
from visigoth.containers.map import Map
from visigoth.map_layers.geoplot import Geoplot, Multipoint, Multiline, Multipolygon
from visigoth.map_layers.gridsquares import GridSquares

class TestGeoplot(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        m1 = Map(512,boundaries=((0,0),(1,1)))
        rng = random.Random(1)

        data1 = [(rng.random(), rng.random()) for x in range(0, 10)]
        data2 = [(rng.random(), rng.random()) for x in range(0, 10)]
        data3 = [(rng.random(), rng.random()) for x in range(0, 10)]
        data4 = [(rng.random(), rng.random()) for x in range(0, 10)]
        multipoints1 = [Multipoint(data1, label="data1", radius=10, fill="red"),
                   Multipoint(data2, label="data2", radius=10,fill="green"),
                   Multipoint(data3, label="data3", radius=10,fill="blue"),
                   Multipoint(data4, label="data4", radius=10, fill="purple")]

        m1.addLayer(Geoplot(multipoints=multipoints1))
        d.add(Box(m1))

        lines1 = [[(rng.random(), rng.random()),(rng.random(), rng.random())] for x in range(0,10)]
        lines2 = [[(rng.random(), rng.random()), (rng.random(), rng.random())] for x in range(0, 10)]
        lines3 = [[(rng.random(), rng.random()), (rng.random(), rng.random())] for x in range(0, 10)]
        lines4 = [[(rng.random(), rng.random()), (rng.random(), rng.random())] for x in range(0, 10)]

        multilines1 = [Multiline(lines1,label="lines1",fill="red"),
                      Multiline(lines2, label="lines2", fill="green"),
                      Multiline(lines3, label="lines3", fill="blue"),
                      Multiline(lines4, label="lines4", fill="purple")]
        m2 = Map(512, boundaries=((0, 0), (1, 1)))
        m2.addLayer(Geoplot(multilines=multilines1))
        d.add(Box(m2))

        squares1 = [[[(x+0.2,y+0.2),(x+0.2,y),(x,y),(x,y+0.2)]] for (x,y) in [(rng.random(), rng.random()) for r in range(0, 10)]]
        squares2 = [[[(x+0.1,y+0.1),(x+0.1,y),(x,y),(x,y+0.1)]] for (x,y) in [(rng.random(), rng.random()) for r in range(0, 10)]]

        multipolys1 = [Multipolygon(squares1,label="squares1",fill="green"),
                      Multipolygon(squares2,label="squares2",fill="red")]
        m3 = Map(512, boundaries=((0, 0), (1, 1)))
        m3.addLayer(Geoplot(multipolys=multipolys1))
        d.add(Box(m3))

        square = [(0.1,0.9),(0.1,0.1),(0.9,0.1),(0.9,0.9)]
        holes = [[(x + 0.1, y + 0.1), (x + 0.1, y), (x, y), (x, y + 0.1)] for (x, y) in
                    [(0.25+0.5*rng.random(), 0.25+0.5*rng.random()) for r in range(0, 10)]]

        multipolys2 = [Multipolygon([[square]+holes], label="squares_with_holes", fill="red")]
        m4 = Map(512, boundaries=((0, 0), (1, 1)))
        m4.addLayer(GridSquares())
        m4.addLayer(Geoplot(multipolys=multipolys2))
        d.add(Box(m4))

        svg = d.draw()
        TestUtils.output(svg,"test_geoplot.svg")
