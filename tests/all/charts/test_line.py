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
from visigoth.utils.colour import DiscretePalette
from visigoth.common import Legend, Text

class TestLine(unittest.TestCase):

    def test_page(self):
        d = Diagram(fill="white")

        d.add(Text("Single-Line"))

        data0 = [(1,0.5),(2,0.3),(3,0.4),(4,0.1),(5,0.7)]
        line0 = Line(data0,x=0,y=1,width=600,height=600)
        d.add(line0)
        
        palette1 = DiscretePalette()
        palette1.addCategory("A","red").addCategory("B","purple").addCategory("C","orange")

        data1 = [(1,11,"A"),(2,11.5,"A"),(3,13.7,"A"),(4,18,"A"),(5,25,"A")]
        data1 += [(1,5,"B"),(2,4.3,"B"),(3,3.2,"B"),(4,5.7,"B"),(5,9.4,"B")]
        data1 += [(1,27,"C"),(2,17,"C"),(3,18.1,"C"),(4,12,"C"),(5,3,"C")]

        d.add(Text("Multi-Line"))
        line1 = Line(data1,x=0,y=1,line=2,colour=2,width=600,height=600,palette=palette1, smoothing=0.3)

        d.add(line1)
        
        legend1 = Legend(palette1,400,legend_columns=2)
        d.add(legend1)
        
        d.connect(legend1,"brushing",line1,"brushing")
        d.connect(line1,"brushing",legend1,"brushing")

        d.add(Text("Custom Axes"))

        data2 = [{"x":2.1,"y":3.4},{"x":2.3,"y":4.5},{"x":2.5,"y":9.0},{"x":2.7,"y":19.3}]
        line2 = Line(data2,x="x",y="y",width=600,height=600,smoothing=0.0)

        (ax,ay) = line2.getAxes()
        ax.setMinValue(2)
        ax.setMaxValue(3)
        ay.setMaxValue(20)
        ay.setMinValue(0)
        
        d.add(line2)
        svg = d.draw()
        TestUtils.output(svg,"test_line.svg")


if __name__ == "__main__":
    unittest.main()

