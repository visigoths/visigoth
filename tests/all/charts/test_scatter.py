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
from visigoth.charts.scatter import Scatter
from visigoth.containers.box import Box

from visigoth.utils.colour import DiscretePalette
from visigoth.common import Legend, Text

class TestScatterPlot(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        palette0 = DiscretePalette()
        palette0.addCategory("A","red")
        palette0.addCategory("B","purple")
        palette0.addCategory("C","orange")


        d = Diagram(fill="white")

        data0 = [
                (1000,800,"p0","A",5),(1200,900,"p1","B",5),(1000,800,"p2","A",5),(200,660,"p3","B",5),
                (700,80,"p4","A",15),(100,200,"p5","B",5),(150,1100,"p6","A",15),(200,500,"p7","C",5),
                (700,700,"p8","C",8),(1200,600,"p9","C",9)]

        d.add(Text("Multi-colour"))

        scatter0 = Scatter(data0, x=0, y=1, label=2, colour=3, size=4, width=500, height=500, palette=palette0)
        (xAxis,yAxis) = scatter0.getAxes()
        xAxis.setLabel("label-x")
        yAxis.setLabel("label-y")

        d.add(Box(scatter0))
        legend0 = Legend(palette0,400,legend_columns=2)
        d.add(legend0)
        d.connect(legend0,"brushing",scatter0,"brushing")
        d.connect(scatter0,"brushing",legend0,"brushing")

        d.add(Text("Monochrome"))
        scatter1 = Scatter(data0, x=0, y=1, label=2, size=4, width=500, height=500)
        d.add(scatter1)

        svg = d.draw()
        TestUtils.output(svg,"test_scatter.svg")

    def test_scatter(self):
        d = Diagram(fill="white")

        d.add(Text("Empty"))

        data0 = []
        scatter0 = Scatter(data0, x=0, y=1, label=2, size=3, width=600, height=600)
        d.add(scatter0)

        svg = d.draw()
        TestUtils.output(svg, "test_emptyscatter.svg")

if __name__ == "__main__":
    unittest.main()