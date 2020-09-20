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
import os

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.map_layers.choropleth import Choropleth
from visigoth.map_layers.wms import WMS
from visigoth.containers.map import Map

from visigoth.containers.box import Box
from visigoth.common.legend import Legend
from visigoth.common.button import Button
from visigoth.common.text import Text
from visigoth.common.space import Space
from visigoth.utils.colour import ContinuousPalette

class TestChoropleth(unittest.TestCase):

    def test_basic(self):
        
        palette = ContinuousPalette()

        rng = random.Random()
        d = Diagram()

        path = os.path.join(os.path.split(__file__)[0],"arrondissements.geojson")

        c = Choropleth(path, lambda props: rng.random() * 10, "name", palette)
        c.setOpacity(0.5)
        # bounds = ((2.0, 48.7),(2.5, 49.1))
        m = Map(512)
        m.add(WMS())
        m.add(c)
        
        d.add(m)
        d.add(Space(20,20))
        d.add(Legend(palette,width=500,legend_columns=3))
        d.add(Text("Attribution: https://www.data.gouv.fr/en/datasets/arrondissements-1/",url="https://www.data.gouv.fr/en/datasets/arrondissements-1/",font_height=18))

        TestUtils.draw_output(d,"test_choropleth")

if __name__ == "__main__":
    unittest.main()
