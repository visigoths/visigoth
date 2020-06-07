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
from visigoth.utils.colour import ContinuousPalette
from visigoth.containers.map import Map
from visigoth.common.legend import Legend
from visigoth.map_layers.kde import KDE
from visigoth.map_layers.scatter import Scatter

from visigoth.utils.mapping import Projections

class TestKDE(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")


        m1 = Map(512,boundaries=((0,0),(1,1)))
        rng = random.Random(1)

        data1 = [(rng.random(), rng.random()) for x in range(0, 100)]

        palette1 = ContinuousPalette()

        m1.addLayer(KDE(data1, bandwidth=4000, nr_samples_across=100, palette=palette1, label_fn=None))
        m1.addLayer(Scatter(data1))
        legend1 = Legend(palette1,512)
        d.add(m1)
        d.add(legend1)

        m2 = Map(512)
        rng = random.Random(1)

        angles = [math.pi * rng.random() * 2 for r in range(50)]
        data2 = [(0.5+0.2*math.sin(a), 0.5+0.2*math.cos(a)) for a in angles]

        palette2 = ContinuousPalette()

        m2.addLayer(KDE(data2, bandwidth=4000, nr_samples_across=100, palette=palette2, label_fn=None))
        m2.addLayer(Scatter(data2))
        legend2 = Legend(palette2, 512)
        d.add(m2)
        d.add(legend2)

        svg = d.draw()
        TestUtils.output(svg,"test_kde.svg")

if __name__ == "__main__":
    unittest.main()
