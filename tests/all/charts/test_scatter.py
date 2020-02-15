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
from visigoth.charts.scatterplot import ScatterPlot
from visigoth.containers.box import Box

from visigoth.utils.colour import DiscretePalette
from visigoth.common.legend import Legend

class TestScatterPlot(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        palette0 = DiscretePalette()
        palette0.addCategory("A","red")
        palette0.addCategory("B","purple")
        palette0.addCategory("C","orange")


        d = Diagram(fill="white")

        data0 = []
        data0.append((1000,800,"p0","A",5))
        data0.append((1200,900,"p1","B",5))
        data0.append((1000,800,"p2","A",5))
        data0.append((200,660,"p3","B",5))
        data0.append((700,80,"p4","A",15))
        data0.append((100,200,"p5","B",5))

        data0.append((150,1100,"p6","A",15))
        data0.append((200,500,"p7","C",5))
        data0.append((700,700,"p8","C",8))
        data0.append((1200,600,"p9","C",9))

        scatter0 = ScatterPlot(data0, 500, 500, palette0, x_axis_label="label-x", y_axis_label="label-y")
        d.add(Box(scatter0))
        legend0 = Legend(palette0,400,legend_columns=2)
        d.add(legend0)
        d.connect(legend0,"brushing",scatter0,"brushing")
        d.connect(scatter0,"brushing",legend0,"brushing")

        palette1 = DiscretePalette()
        palette1.addCategory("A","green")
        palette1.addCategory("B","blue")
        palette1.addCategory("C","yellow")

        data1 = []
        data1.append((-1000,800,"p0","A",25))
        data1.append((1200,-900,"p1","B",25))
        data1.append((1000,800,"p2","A",25))
        data1.append((200,-660,"p3","B",15))
        data1.append((700,80,"p4","A",15))
        data1.append((-100,200,"p5","B",5))

        data1.append((150,-1100,"p6","A",15))
        data1.append((200,500,"p7","C",5))
        data1.append((700,-700,"p8","C",18))
        data1.append((-1200,600,"p9","C",19))

        data1.append((250,-100,"p10","A",15))
        data1.append((0,0,"p7","p11",5))
        data1.append((50,-150,"p12","C",18))
        data1.append((-500,600,"p13","C",25))

        scatter1 = ScatterPlot(data1, 700, 500, palette1, x_axis_label="label-x", y_axis_label="label-y")
        d.add(Box(scatter1))

        legend1 = Legend(palette1,400,legend_columns=2)
        d.add(legend1)
        d.connect(legend1,"brushing",scatter1,"brushing")
        d.connect(scatter1,"brushing",legend1,"brushing")
        svg = d.draw()
        TestUtils.output(svg,"test_scatter.svg")

    def test_empty(self):
        d = Diagram(fill="white")

        palette0 = DiscretePalette()
        palette0.addCategory("A","red")
        palette0.addCategory("B","purple")
        palette0.addCategory("C","orange")

        d = Diagram(fill="white")

        data0 = []

        scatter0 = ScatterPlot(data0, 300, 300, palette0, x_axis_label="label-x", y_axis_label="label-y")
        d.add(scatter0)
        legend0 = Legend(palette0,300,legend_columns=2)
        d.add(legend0)
        d.connect(legend0,"brushing",scatter0,"brushing")
        d.connect(scatter0,"brushing",legend0,"brushing")

        palette1 = DiscretePalette()
        palette1.addCategory("A","green")
        palette1.addCategory("B","blue")
        palette1.addCategory("C","yellow")

        data1 = []
        data1.append((0,0,"p0","A",25))

        scatter1 = ScatterPlot(data1, 300, 300, palette1, x_axis_label="label-x", y_axis_label="label-y")
        d.add(scatter1)

        legend1 = Legend(palette1,300,legend_columns=2)
        d.add(legend1)
        d.connect(legend1,"brushing",scatter1,"brushing")
        d.connect(scatter1,"brushing",legend1,"brushing")
        svg = d.draw()
        TestUtils.output(svg,"test_scatter_empty.svg")



