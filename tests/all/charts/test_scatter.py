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
from visigoth.charts.scatter import Scatter
from visigoth.containers.box import Box

from visigoth.utils.colour import DiscreteColourManager
from visigoth.common import Legend, Text

class TestScatterPlot(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        colour_manager0 = DiscreteColourManager()
        colour_manager0.addColour("A","red")
        colour_manager0.addColour("B","purple")
        colour_manager0.addColour("C","orange")


        d = Diagram(fill="white")

        data0 = [
                (1000,800,"p0","A",5),(1200,900,"p1","B",5),(1000,800,"p2","A",5),(200,660,"p3","B",5),
                (700,80,"p4","A",15),(100,200,"p5","B",5),(150,1100,"p6","A",15),(200,500,"p7","C",5),
                (700,700,"p8","C",8),(1200,600,"p9","C",9)]

        d.add(Text("Multi-colour"))

        scatter0 = Scatter(data0, x=0, y=1, label=2, colour=3, size=4, width=500, height=500, colour_manager=colour_manager0)
        (xAxis,yAxis) = scatter0.getAxes()
        xAxis.setLabel("label-x")
        yAxis.setLabel("label-y")

        d.add(Box(scatter0))
        legend0 = Legend(colour_manager0,400,legend_columns=2)
        d.add(legend0)
        d.connect(legend0,"colour",scatter0,"colour")
        d.connect(scatter0,"colour",legend0,"colour")

        d.add(Text("Monochrome"))
        scatter1 = Scatter(data0, x=0, y=1, label=2, size=4, width=500, height=500)
        d.add(scatter1)

        TestUtils.draw_output(d,"test_scatter")

    def test_scatter(self):
        d = Diagram(fill="white")

        d.add(Text("Empty"))

        data0 = []
        scatter0 = Scatter(data0, x=0, y=1, label=2, size=3, width=600, height=600)
        d.add(scatter0)

        TestUtils.draw_output(d, "test_emptyscatter")

if __name__ == "__main__":
    unittest.main()