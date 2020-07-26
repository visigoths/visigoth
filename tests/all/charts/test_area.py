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
import math

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.charts.area import Area
from visigoth.utils.colour import DiscretePalette
from visigoth.common import Legend, Text
from visigoth.containers import Grid,Sequence

class TestArea(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        dp = DiscretePalette()

        data = [
            (1,12,"A"),
            (2,14,"A"),
            (3,11,"A"),
            (4,9,"A"),
            (5,7,"A"),
            (1,2,"B"),
            (2,4,"B"),
            (3,7,"B"),
            (4,10,"B"),
            (5,11,"B"),
            (1,2,"C"),
            (2,3,"C"),
            (3,1,"C"),
            (4,3,"C"),
            (5,2,"C")
        ]

        d.add(Text("Individual areas"))

        g = Grid()
        row = 0
        col = 0
        for cat in ["A","B","C"]:
            s = Sequence()            
            s.add(Text(cat))
            area0 = Area([d for d in data if d[2] == cat], x=0, y=1, palette=dp, height=300, width=300)
            s.add(area0)
            g.add(row,col,s)
            col += 1
            if col == 2:
                row += 1
                col = 0        
        d.add(g)

        d.add(Text("Smoothing"))

        d.add(Text("Stacked areas"))
        area1 = Area(data, x=0, y=1, size=1, colour=2, height=600, palette=dp, width=600)
        d.add(area1)

        legend1 = Legend(dp,400,legend_columns=2)
        d.add(legend1)
        d.connect(legend1,"colour",area1,"colour")
        d.connect(area1,"colour",legend1,"colour")
        
        for smoothing in [0.1,0.3,0.5]:
            d.add(Text("Smoothing=%f"%(smoothing)))
            area2 = Area(data, x=0, y=1, colour=2, height=400, smoothing=smoothing, palette=dp, width=400)
            d.add(area2)

        TestUtils.draw_output(d,"test_area")

    def test_empty(self):
        d = Diagram(fill="white")

        d.add(Text("Empty"))

        data0 = []
        area0 = Area(data0, x=0, y=1, size=1, colour=2, height=600, width=600)
        d.add(area0)
        TestUtils.draw_output(d, "test_emptyarea")

if __name__ == "__main__":
    unittest.main()