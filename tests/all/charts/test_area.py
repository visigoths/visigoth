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
import math

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.charts.area import Area
from visigoth.common.space import Space
from visigoth.utils.colour import DiscretePalette
from visigoth.common.legend import Legend
from visigoth.common.space import Space

class TestBar(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        palette0 = DiscretePalette()
        palette0.addCategory("A","#E7FFAC")
        palette0.addCategory("B","#FFC9DE")
        palette0.addCategory("C","#B28DFF")
        palette0.addCategory("D","#ACE7FF")

        data0 = []

        for idx in range(0,32):
            linedata = {}
            angle = idx/2.0
            for cat in ["A","B","C","D"]:
                if cat == "B" or cat == "C":
                    angle += math.pi/4

                if cat == "A" or cat == "C":
                    h = 1.5+math.sin(angle)
                else:
                    h = 1.5+math.cos(angle)
                linedata[cat]=("",h)
            data0.append((angle,linedata))

        area0 = Area(data0, 600, 600, palette0, negcats=["C","D"],x_axis_label="X", y_axis_label="Y")

        d.add(area0)
        legend0 = Legend(palette0,400,legend_columns=2)
        d.add(legend0)
        d.connect(legend0,"brushing",area0,"brushing")
        d.connect(area0,"brushing",legend0,"brushing")
        svg = d.draw()
        TestUtils.output(svg,"test_area.svg")

