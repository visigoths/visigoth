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
from visigoth.map_layers.cartogram import Cartogram
from visigoth.containers.map import Map
from visigoth.containers.box import Box
from visigoth.common.legend import Legend
from visigoth.utils.mapping.projections import Projections
from visigoth.utils.colour import DiscretePalette

class TestCartogram(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        rng = random.Random(3)

        def gen(cx,cy,minr,maxr):
            radius = minr+rng.random()*(maxr-minr)
            cat = random.choice(["cat1", "cat2", "cat3"])
            label = "cat: "+cat
            return (cx,cy,cat,label,radius)

        palette = DiscretePalette()
        palette.addCategory("cat1","yellow")
        palette.addCategory("cat2","green")
        palette.addCategory("cat3","purple")

        data = [gen(cx,cy,10,25) for (cx,cy) in [(0.25,0.25),(0.75,0.75),(0.25,0.75),(0.75,0.25)] for _ in range(0,25)]

        bounds  = ((0.0,0.0),(1.0,1.0))
        m = Map(512,bounds,projection=Projections.IDENTITY)
        c = Cartogram(data, palette, iterations=500, stroke_width=2, stroke="black", link_stroke="red")
        m.addLayer(c)
        legend = Legend(palette, width=500, legend_columns=3)
        d.add(Box(m))
        d.add(legend)

        d.connect(c,"brushing",legend,"brushing")
        d.connect(legend,"brushing",c,"brushing")

        svg = d.draw()

        TestUtils.output(svg,"test_cartogtam.svg")
        