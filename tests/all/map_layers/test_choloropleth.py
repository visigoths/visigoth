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
import os

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.map_layers.chloropleth import Chloropleth
from visigoth.map_layers.wms import WMS
from visigoth.containers.map import Map

from visigoth.containers.box import Box
from visigoth.common.legend import Legend
from visigoth.common.button import Button
from visigoth.common.text import Text
from visigoth.common.space import Space
from visigoth.utils.colour import ContinuousPalette

class TestChloropleth(unittest.TestCase):

    def test_basic(self):
        
        palette = ContinuousPalette()
        palette.addColour("red",0.0).addColour("purple",10.0)

        rng = random.Random()
        d = Diagram()

        path = os.path.join(os.path.split(__file__)[0],"arrondissements.geojson")

        c = Chloropleth(path,lambda props:rng.random()*10,"name",palette)
        c.setOpacity(0.5)
        # bounds = ((2.0, 48.7),(2.5, 49.1))
        m = Map(512)
        m.addLayer(WMS())
        m.addLayer(c)
        
        d.add(m)
        d.add(Space(20,20))
        d.add(Legend(palette,width=500,legend_columns=3))
        d.add(Text("Attribution: https://www.data.gouv.fr/en/datasets/arrondissements-1/",url="https://www.data.gouv.fr/en/datasets/arrondissements-1/",font_height=18))
        svg = d.draw()
        TestUtils.output(svg,"test_chloropleth.svg")

if __name__ == "__main__":
    unittest.main()
