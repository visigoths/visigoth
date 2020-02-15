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
        m = Map(512,bounds,projection=Projections.ESPG_3857)
        c = Compass()
        w = WMS()
        m.addLayer(w)
        m.addLayer(c)
        d.add(Box(m))
    
        svg = d.draw()
        TestUtils.output(svg,"test_compass.svg")

if __name__ == '__main__':
    tg = TestCompass()
    tg.test_basic()