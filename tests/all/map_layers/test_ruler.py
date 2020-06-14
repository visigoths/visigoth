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
from visigoth.map_layers.ruler import Ruler
from visigoth.utils.mapping import Projections,Mapping

class TestRuler(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        center0 = (0,0)
        bounds0 = Mapping.computeBoundaries(center0,4000,projection=Projections.EPSG_3857)
        m0 = Map(256,boundaries=bounds0,projection=Projections.EPSG_3857)
        r0 = Ruler()
        m0.addLayer(r0)
        d.add(Box(m0))

        center1 = (10,10)
        bounds1 = Mapping.computeBoundaries(center1,40000,projection=Projections.EPSG_3857)
        m1 = Map(256,boundaries=bounds1,projection=Projections.EPSG_3857)
        r1 = Ruler(stroke="red",font_height=36,stroke_width=5)
        m1.addLayer(r1)
        d.add(Box(m1))

        center2 = (10,10)
        bounds2 = Mapping.computeBoundaries(center2,1000,projection=Projections.EPSG_3857)
        m2 = Map(512,boundaries=bounds2,projection=Projections.EPSG_3857)
        r2 = Ruler()
        m2.addLayer(r2)
        d.add(Box(m2))

        bounds3 = ((0,0),(5,10))
        m3 = Map(512,boundaries=bounds3,projection=Projections.IDENTITY,font_height=18)
        r3 = Ruler()
        m3.addLayer(r3)
        d.add(Box(m3))
        svg = d.draw()
        TestUtils.output(svg,"test_ruler.svg")

if __name__ == "__main__":
    unittest.main()
