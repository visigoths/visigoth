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
from visigoth.common.text import Text
from visigoth.containers.sequence import Sequence

from visigoth.map_layers.wms import WMS
from visigoth.utils.mapping import Geocoder
from visigoth.utils.mapping import Projections, Mapping


class TestDiagram(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="lightblue",margin_left=10,margin_right=10,spacing=5)

        d.addStyle(":focus { outline: 2px solid purple }\n"+
            ".highlight { stroke: purple;stroke-width:2px; }")

        d.setDefaultTextAttributes({"font-family":"sans-serif","font-weight":"bold"})
        gc = Geocoder()
        center = gc.fetchCenter("Berlin")
        bounds=Mapping.computeBoundaries(center,4000,projection=Projections.EPSG_3857)

        m1 = Map(768, boundaries=bounds, projection=Projections.EPSG_3857)

        wms1 = WMS(type="osm")
        wms1.setInfo("Map")

        m1.add(wms1)

        s1 = Sequence()
        s1.add(m1)

        d.add(Box(Text("Berlin Map",font_height=32),fill="white"))
        d.add(Box(s1,fill="white"))

        TestUtils.draw_output(d,"test_diagram")

if __name__ == '__main__':
    thb = TestDiagram()
    thb.test_basic()
    