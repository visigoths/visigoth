# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.containers.box import Box
from visigoth.containers.map import Map
from visigoth.map_layers.ruler import Ruler
from visigoth.utils.mapping import Projections,Mapping

class TestRuler(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        center0 = (0,0)
        bounds0 = Mapping.computeBoundaries(center0,4000,projection=Projections.EPSG_3857)
        m0 = Map(256,boundaries=bounds0,projection=Projections.EPSG_3857)
        r0 = Ruler()
        m0.add(r0)
        d.add(Box(m0))

        center1 = (10,10)
        bounds1 = Mapping.computeBoundaries(center1,40000,projection=Projections.EPSG_3857)
        m1 = Map(256,boundaries=bounds1,projection=Projections.EPSG_3857)
        r1 = Ruler(stroke="red",font_height=36,stroke_width=5)
        m1.add(r1)
        d.add(Box(m1))

        center2 = (10,10)
        bounds2 = Mapping.computeBoundaries(center2,1000,projection=Projections.EPSG_3857)
        m2 = Map(512,boundaries=bounds2,projection=Projections.EPSG_3857)
        r2 = Ruler()
        m2.add(r2)
        d.add(Box(m2))

        bounds3 = ((0,0),(5,10))
        m3 = Map(512,boundaries=bounds3,projection=Projections.IDENTITY,font_height=18)
        r3 = Ruler()
        m3.add(r3)
        d.add(Box(m3))

        TestUtils.draw_output(d,"test_ruler")

if __name__ == "__main__":
    unittest.main()
