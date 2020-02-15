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
from visigoth.containers.box import Box
from visigoth.containers.map import Map
from visigoth.map_layers.gridsquares import GridSquares
from visigoth.utils.mapping import Projections, Mapping

class TestGridSquares(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        center0 = (0,0)
        bounds0 = Mapping.computeBoundaries(center0,4000,projection=Projections.ESPG_3857)
        m0 = Map(256,boundaries=bounds0,projection=Projections.ESPG_3857)
        grid0 = GridSquares()
        m0.addLayer(grid0)
        d.add(Box(m0))

        center1 = (10,10)
        bounds1 = Mapping.computeBoundaries(center1,40000,projection=Projections.ESPG_3857)
        m1 = Map(256,boundaries=bounds1,projection=Projections.ESPG_3857)
        grid1 = GridSquares()
        m1.addLayer(grid1)
        d.add(Box(m1))

        center2 = (10,10)
        bounds2 = Mapping.computeBoundaries(center2,80000,projection=Projections.ESPG_3857)
        m2 = Map(512,boundaries=bounds2,projection=Projections.ESPG_3857)
        grid2 = GridSquares()
        m2.addLayer(grid2)
        d.add(Box(m2))
        svg = d.draw()

        bounds3 = ((0,0),(5,10))
        m3 = Map(512,boundaries=bounds3,projection=Projections.IDENTITY,font_height=18)
        grid3 = GridSquares()
        m3.addLayer(grid3)
        d.add(Box(m3))
        svg = d.draw()
        TestUtils.output(svg,"test_gridsquares.svg")
