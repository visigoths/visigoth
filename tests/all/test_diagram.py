# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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
        bounds=Mapping.computeBoundaries(center,4000,projection=Projections.ESPG_3857)

        m1 = Map(768, boundaries=bounds, projection=Projections.ESPG_3857)

        wms1 = WMS(type="osm")
        wms1.setInfo("Map")

        m1.addLayer(wms1)

        s1 = Sequence()
        s1.add(m1)

        d.add(Box(Text("Berlin Map",font_height=32),fill="white"))
        d.add(Box(s1,fill="white"))

        svg = d.draw(include_footer=False)
        TestUtils.output(svg,"test_diagram.svg")

if __name__ == '__main__':
    thb = TestDiagram()
    thb.test_basic()
    