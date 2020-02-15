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

class TestScatter(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        m1 = Map(512,boundaries=((0,0),(1,1)))
        rng = random.Random(1)

        data1 = [(rng.random(), rng.random()) for x in range(0, 100)]

        m1.addLayer(Scatter(data1))
        d.add(Box(m1))

        m2 = Map(512, boundaries=((0, 0), (1, 1)))
        rng = random.Random(1)

        angles1 = [math.pi * rng.random() * 2 for r in range(50)]
        angles2 = [math.pi * rng.random() * 2 for r in range(50)]
        data2a = [(0.5+0.3*rng.random()*math.sin(a), 0.5+0.3*rng.random()*math.cos(a)) for a in angles1]
        data2b = [(0.5 + 0.4 * math.sin(a), 0.5 + 0.4 * math.cos(a)) for a in angles2]

        m2.addLayer(Scatter(data2a,fill="green"))
        m2.addLayer(Scatter(data2b, fill="orange",radius=20,stroke="red",stroke_width=3))

        d.add(Box(m2))

        svg = d.draw()
        TestUtils.output(svg,"test_scatter.svg")

if __name__ == '__main__':
    s = TestScatter()
    s.test_basic()