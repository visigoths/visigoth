# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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
        palette1.addColour("A","red").addColour("B","purple").addColour("C","orange")

        data1 = [(1,11,"A"),(2,11.5,"A"),(3,13.7,"A"),(4,18,"A"),(5,25,"A")]
        data1 += [(1,5,"B"),(2,4.3,"B"),(3,3.2,"B"),(4,5.7,"B"),(5,9.4,"B")]
        data1 += [(1,27,"C"),(2,17,"C"),(3,18.1,"C"),(4,12,"C"),(5,3,"C")]

        d.add(Text("Multi-Line"))
        line1 = Line(data1,x=0,y=1,colour=2,width=600,height=600,palette=palette1, smoothing=0.3)

        d.add(line1)
        
        legend1 = Legend(palette1,400,legend_columns=2)
        d.add(legend1)
        
        d.connect(legend1,"colour",line1,"colour")
        d.connect(line1,"colour",legend1,"colour")

        d.add(Text("Custom Axes"))

        data2 = [{"x":2.1,"y":3.4},{"x":2.3,"y":4.5},{"x":2.5,"y":9.0},{"x":2.7,"y":19.3}]
        line2 = Line(data2,x="x",y="y",width=600,height=600,smoothing=0.0)

        (ax,ay) = line2.getAxes()
        ax.setMinValue(2)
        ax.setMaxValue(3)
        ay.setMaxValue(20)
        ay.setMinValue(0)
        
        d.add(line2)
        TestUtils.draw_output(d,"test_line")

    def test_empty(self):
        d = Diagram(fill="white")

        d.add(Text("Empty"))

        data0 = []
        line0 = Line(data0, x=0, y=1, width=600, height=600)
        (ax, ay) = line0.getAxes()
        ax.setMinValue(0.0)
        ax.setMaxValue(3.0)
        ay.setMaxValue(20.0)
        ay.setMinValue(0.0)
        d.add(line0)

        TestUtils.draw_output(d, "test_emptyline")


if __name__ == "__main__":
    unittest.main()

