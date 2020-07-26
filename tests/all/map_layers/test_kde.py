# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

        m1.add(KDE(data1, bandwidth=4000, nr_samples_across=100, palette=palette1, label_fn=None))
        m1.add(Scatter(data1))
        legend1 = Legend(palette1,512)
        d.add(m1)
        d.add(legend1)

        m2 = Map(512)
        rng = random.Random(1)

        angles = [math.pi * rng.random() * 2 for r in range(50)]
        data2 = [(0.5+0.2*math.sin(a), 0.5+0.2*math.cos(a)) for a in angles]

        palette2 = ContinuousPalette()

        m2.add(KDE(data2, bandwidth=4000, nr_samples_across=100, palette=palette2, label_fn=None))
        m2.add(Scatter(data2))
        legend2 = Legend(palette2, 512)
        d.add(m2)
        d.add(legend2)

        TestUtils.draw_output(d,"test_kde")

if __name__ == "__main__":
    unittest.main()
