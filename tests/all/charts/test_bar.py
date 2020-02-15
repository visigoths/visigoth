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
from visigoth.charts.bar import Bar
from visigoth.common.space import Space
from visigoth.utils.colour import DiscretePalette
from visigoth.common.legend import Legend
from visigoth.common.space import Space

class TestBar(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        palette0 = DiscretePalette()
        palette0.addCategory("A","#E7FFAC").addCategory("B","#FFC9DE")
        palette0.addCategory("C","#B28DFF").addCategory("D","#ACE7FF")

        data0 = [("A",1.2),("B",0),("C",-0.4),("D",0.5)]

        bar0 = Bar(data0, 400, 400, palette0,labelfn=lambda k,v:"%0.2f"%v)
        d.add(bar0).add(Space(20))
        legend0 = Legend(palette0,400,legend_columns=2)
        d.add(legend0).add(Space(20))
        d.connect(legend0,"brushing",bar0,"brushing")
        d.connect(bar0,"brushing",legend0,"brushing")

        palette1 = DiscretePalette()
        palette1.addCategory("A","#E7FFAC")
        palette1.addCategory("B1","red").addCategory("B2","green")
        palette1.addCategory("C","#B28DFF")
        palette1.addCategory("D1","orange").addCategory("D2","purple")

        data1 = [("A",10),("B",[("B1",5),("B2",15)]),("C",-4),("D",[("D1",-5),("D2",-2)])]

        bar1 = Bar(data1, 400, 400, palette1,labelfn=lambda k,v:"%d"%v)
        d.add(bar1).add(Space(20))
        legend1 = Legend(palette1,400,legend_columns=2)
        d.add(legend1)
        d.connect(legend1,"brushing",bar1,"brushing")
        d.connect(bar1,"brushing",legend1,"brushing")
        svg = d.draw()
        TestUtils.output(svg,"test_bar.svg")

    def test_waterfall(self):
        d = Diagram(fill="white")

        palette = DiscretePalette()
        palette.addCategory("A","#E7FFAC")
        palette.addCategory("B","#FFC9DE")
        palette.addCategory("C","#B28DFF")
        palette.addCategory("D","#ACE7FF")

        data = [("A",10),("B",5),("C",-4),("D",-25)]

        bar = Bar(data, 400, 400, palette,waterfall=True,draw_axis=True,draw_grid=False,labelfn=lambda k,v:"%d"%v)
        d.add(bar).add(Space(20))
        legend = Legend(palette,400,legend_columns=2)
        d.add(legend)
        d.connect(legend,"brushing",bar,"brushing")
        d.connect(bar,"brushing",legend,"brushing")
        svg = d.draw()
        TestUtils.output(svg,"test_bar_waterfall.svg")
