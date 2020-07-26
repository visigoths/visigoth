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
from visigoth.containers.box import Box
from visigoth.containers.map import Map
from visigoth.map_layers.geoplot import Geoplot, Multipoint, Multiline, Multipolygon
from visigoth.map_layers import WMS
from visigoth.utils.mapping.projections import Projections

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

        m1.add(Geoplot(multipoints=multipoints1))
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
        m2.add(Geoplot(multilines=multilines1))
        d.add(Box(m2))

        squares1 = [[[(x+0.2,y+0.2),(x+0.2,y),(x,y),(x,y+0.2)]] for (x,y) in [(rng.random(), rng.random()) for r in range(0, 10)]]
        squares2 = [[[(x+0.1,y+0.1),(x+0.1,y),(x,y),(x,y+0.1)]] for (x,y) in [(rng.random(), rng.random()) for r in range(0, 10)]]

        multipolys1 = [Multipolygon(squares1,label="squares1",fill="green"),
                      Multipolygon(squares2,label="squares2",fill="red")]
        m3 = Map(512, boundaries=((0, 0), (1, 1)))
        m3.add(Geoplot(multipolys=multipolys1))
        d.add(Box(m3))

        square = [(0.1,0.9),(0.1,0.1),(0.9,0.1),(0.9,0.9)]
        holes = [[(x + 0.1, y + 0.1), (x + 0.1, y), (x, y), (x, y + 0.1)] for (x, y) in
                    [(0.25+0.5*rng.random(), 0.25+0.5*rng.random()) for r in range(0, 10)]]

        multipolys2 = [Multipolygon([[square]+holes], label="squares_with_holes", fill="red")]
        m4 = Map(512, boundaries=((0, 0), (1, 1)))
        m4.add(Geoplot(multipolys=multipolys2))
        d.add(Box(m4))

        TestUtils.draw_output(d,"test_geoplot")

    def test_geoplot_world(self):
        d = Diagram(fill="white")

        wm = Map(width=1024, boundaries=((-180, -90), (180, 90)), projection=Projections.EPSG_4326)

        def make_box(lon_min,lat_min,lon_max,lat_max):
            b = []
            b.append((lon_min, lat_min))
            b.append((lon_max, lat_min))
            b.append((lon_max, lat_max))
            b.append((lon_min, lat_max))
            return b

        vb1 = make_box(-10,40,10,60)
        sw = make_box(-180, -90, -170, -80)
        se = make_box(170, -90, 180, -80)
        ne = make_box(170, 80, 180, 90)
        nw = make_box(-180, 80, -170, 90)

        poly = Multipolygon([[vb1],[ne],[nw],[se],[sw]], stroke_width=0, fill="#FF000080")

        wm.add(WMS())
        geoplot = Geoplot(multipolys=[poly])
        wm.add(geoplot)
        d.add(wm)

        TestUtils.draw_output(d, "test_geoplot_world")


if __name__ == "__main__":
    unittest.main()
