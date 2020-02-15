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
import random
import math

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.containers.map import Map
from visigoth.containers.box import Box
from visigoth.map_layers.scatter import Scatter
from visigoth.map_layers.voronoi import Voronoi
from visigoth.utils.colour import Colour

class TestVoronoi(unittest.TestCase):

    def test_basic(self):
        d = Diagram()

        m1 = Map(512)
        rng = random.Random(1)

        data1 = [(rng.random(), rng.random()) for x in range(0, 100)]
        data1v = [(x,y,Colour.randomColour(),"") for (x,y) in data1]
        m1.addLayer(Scatter(data1))
        m1.addLayer(Voronoi(data1v))
        d.add(Box(m1))

        m2 = Map(512)
        rng = random.Random(1)

        angles2 = [math.pi * rng.random() * 2 for r in range(15)]

        data2 = [(0.5 + (0.4+0.1*rng.random())*math.sin(a), 0.5 + (0.4 + 0.1*rng.random())*math.cos(a)) for a in angles2]
        data2v = [(x,y,Colour.randomColour(),"") for (x,y) in data2]

        m2.addLayer(Voronoi(data2v,radius=8,stroke="red",stroke_width=2))
        m2.addLayer(Scatter(data2,fill="green"))

        d.add(Box(m2))

        svg = d.draw()
        TestUtils.output(svg,"test_voronoi.svg")

    def test_square(self):
        d = Diagram()

        m1 = Map(512)

        data1 = [(0.25,0.25,Colour.randomColour(),""),(0.75,0.75,Colour.randomColour(),""),(0.25,0.75,Colour.randomColour(),""),(0.75,0.25,Colour.randomColour(),"")]
        m1.addLayer(Voronoi(data1))
        d.add(Box(m1))

        svg = d.draw()
        TestUtils.output(svg,"test_voronoi_square.svg")


if __name__ == '__main__':
    thb = TestVoronoi()
    thb.test_basic()
    thb.test_square()