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
from visigoth.charts.pie import Pie
from visigoth.common.space import Space
from visigoth.utils.colour import DiscretePalette
from visigoth.common.legend import Legend
from visigoth.common.space import Space

class TestPie(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        palette0 = DiscretePalette()
        palette0.addCategory("category A","#E7FFAC").addCategory("category B","#FFC9DE")
        palette0.addCategory("category C","#B28DFF").addCategory("category D","#ACE7FF")

        data0 = [("category A",1.2),("category B",0.1),("category C",0.4),("category D",0.5)]
        pie0 = Pie(data0, 400, 400, palette0, doughnut=True)
        d.add(pie0)

        pie1 = Pie(data0, 400, 400, palette0)
        d.add(pie1)

        legend0 = Legend(palette0,400,legend_columns=1)
        d.add(legend0)
        svg = d.draw()
        TestUtils.output(svg,"test_pie.svg")

    def test_multilevel(self):

        d = Diagram(fill="white")

        palette0 = DiscretePalette()
        palette0.addCategory("category A","#E7FFAC").addCategory("category B","#FFC9DE")
        palette0.addCategory("category C","#B28DFF").addCategory("category D","#ACE7FF")
        palette0.addCategory("category B.1","lightgrey").addCategory("category B.2","darkgrey")
        palette0.addCategory("category D.1","lightgreen").addCategory("category D.2","darkgreen").addCategory("category D.3","green")

        data0 = [("category A",10),
            ("category B",[("category B.1",15),("category B.2",5)]),
            ("category C",4),
            ("category D",[("category D.1",12),("category D.2",3),("category D.3",5)])]

        pie0 = Pie(data0, 600, 600, palette0, doughnut=True)
        d.add(pie0)
        legend0 = Legend(palette0,400,legend_columns=2)
        d.add(legend0)
        d.connect(legend0,"brushing",pie0,"brushing")
        d.connect(pie0,"brushing",legend0,"brushing")
        svg = d.draw()
        TestUtils.output(svg,"test_pie_multilevel.svg")


tp = TestPie()
tp.test_basic()