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

from visigoth.diagram import Diagram
from visigoth.containers.map import Map
from visigoth.containers.box import Box
from visigoth.map_layers.compass import Compass
from visigoth.map_layers.wms import WMS
from visigoth.utils.mapping.projections import Projections
from visigoth.utils.test_utils import TestUtils

class TestCompass(unittest.TestCase):

    def test_basic(self):

        d = Diagram()
        bounds  = ((-180,-60),(180,60))
        m = Map(512,bounds,projection=Projections.EPSG_3857)
        c = Compass()
        w = WMS()
        m.add(w)
        m.add(c)
        d.add(Box(m))

        TestUtils.draw_output(d,"test_compass")

if __name__ == "__main__":
    unittest.main()
