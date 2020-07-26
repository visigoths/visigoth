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
from visigoth.charts.bar import Bar
from visigoth.common.space import Space
from visigoth.utils.colour import DiscretePalette
from visigoth.common.legend import Legend
from visigoth.common.space import Space

class TestBar(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        palette0 = DiscretePalette()
        
        data0 = [("A",1.2),("B",0),("C",-0.4),("D",0.5)]

        bar0 = Bar(data0, x=0, y=1, colour=0, width=400, height=400, palette=palette0,labelfn=lambda k,v:"%0.2f"%v)
        d.add(bar0)
        legend0 = Legend(palette0,400,legend_columns=2)
        d.add(legend0)
        d.connect(legend0,"colour",bar0,"colour")
        d.connect(bar0,"colour",legend0,"colour")

        palette1 = DiscretePalette()
        
        data1 = [("A",10,"A"),("B",25,"B"),("C",4,"C"),("D",5,"D1"),("D",2,"D2")]

        bar1 = Bar(data1,x=0,y=1,colour=2,width=400, height=400, palette=palette1,labelfn=lambda k,v:"%d"%v)
        d.add(bar1)
        legend1 = Legend(palette1,400,legend_columns=2)
        d.add(legend1)
        d.connect(legend1,"colour",bar1,"colour")
        d.connect(bar1,"colour",legend1,"colour")
        svg = d.draw()
        TestUtils.output(svg,"test_bar.svg")

        bar2 = Bar(data1, x=0, y=1, colour=2, stacked=False, width=400, height=400, palette=palette1)
        d.add(bar2)
        legend2 = Legend(palette1, 400, legend_columns=2)
        d.add(legend2)
        d.connect(legend2, "colour", bar2, "colour")
        d.connect(bar2, "colour", legend2, "colour")
        TestUtils.draw_output(d, "test_bar")

    def test_nopalette(self):
        d = Diagram(fill="white")
        data = [("A",10),("B",5),("C",-4),("D",-25)]
        bar = Bar(data,x=0,y=1,width=400,height=400,labelfn=lambda k,v:"%d"%v)
        d.add(bar)
        TestUtils.draw_output(d,"test_bar_nopalette")

if __name__ == "__main__":
    unittest.main()