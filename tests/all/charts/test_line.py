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
from visigoth.charts.line import Line
from visigoth.common.space import Space
from visigoth.utils.colour import DiscretePalette
from visigoth.common.legend import Legend
from visigoth.common.space import Space

class TestLine(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        palette0 = DiscretePalette()
        palette0.addCategory("A","red")
        palette0.addCategory("B","purple")
        palette0.addCategory("C","orange")

        data0 = []
        data0 += [(1,11,"A"),(2,11.5,"A"),(3,13.7,"A"),(4,18,"A"),(5,25,"A")]
        data0 += [(1,5,"B"),(2,4.3,"B"),(3,3.2,"B"),(4,5.7,"B"),(5,9.4,"B")]
        data0 += [(1,27,"C"),(2,17,"C"),(3,18.1,"C"),(4,12,"C"),(5,3,"C")]

        d = Diagram(fill="white")

        line0 = Line(data0,x=0,y=1,line=2,colour=2,width=600,height=600,palette=palette0, x_axis_label="label_x", y_axis_label="label_y")

        d.add(line0)
        d.add(Space(20))
        legend0 = Legend(palette0,400,legend_columns=2)
        d.add(legend0)
        d.connect(legend0,"brushing",line0,"brushing")
        d.connect(line0,"brushing",legend0,"brushing")
        svg = d.draw()
        TestUtils.output(svg,"test_line.svg")


if __name__ == "__main__":
    unittest.main()

