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
import os.path

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.containers.map import Map
from visigoth.containers.box import Box
from visigoth.map_layers.geoimport import Geoimport
from visigoth.map_layers.wms import WMS

class TestGeoimport(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        m1 = Map(512)

        path = os.path.join(os.path.split(__file__)[0],"Berlin_gemeinden_simplify0.geojson")
        m1.addLayer(WMS())
        m1.addLayer(Geoimport(path=path,polygon_style={"fill":"#FFFFFF30"}))
        d.add(Box(m1))

        svg = d.draw()
        TestUtils.output(svg,"test_geoimport.svg")

if __name__ == "__main__":
    unittest.main()
