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

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.containers.map import Map
from visigoth.containers.box import Box
from visigoth.map_layers.wmts import WMTS
from visigoth.map_layers.geoplot import Geoplot, Multipoint

class TestWMTS(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        bounds = ((166.509144322, -46.641235447), (178.517093541, -34.4506617165))

        m = Map(512, bounds)
        m.addLayer(WMTS())

        # add marker for Christchurch
        m.addLayer(Geoplot(multipoints=[Multipoint([(172.639847,-43.525650)],marker=True)]))
        d.add(Box(m))

        svg = d.draw()
        TestUtils.output(svg,"test_wmts.svg")