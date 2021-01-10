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
from visigoth.charts.pie import Pie
from visigoth.utils.colour import DiscreteColourManager
from visigoth.common import Legend, Text
from visigoth.containers import Box

class TestPie(unittest.TestCase):

    def test_page(self):
        d = Diagram(fill="white")

        d.add(Text("Basic"))
        colour_manager0 = DiscreteColourManager()
        colour_manager0.addColour("category A","#E7FFAC").addColour("category B","#FFC9DE")
        colour_manager0.addColour("category C","#B28DFF").addColour("category D","#ACE7FF")

        data0 = [("category A",1.2),("category B",0.1),("category C",0.4),("category D",0.5)]
        pie0 = Pie(data0, value=1,colour=0, width=400, height=400, colour_manager=colour_manager0)
        d.add(Box(pie0))

        legend0 = Legend(colour_manager0,400,legend_columns=1)
        d.add(legend0)

        d.add(Text("Basic (Count)"))
        
        data0a = [("Cars",),("Cars",),("Cars",),("Bikes",),("Bikes",),("Trucks",),("Bikes",),("Bikes",)]
        pie0a = Pie(data0a, colour=0, width=300, height=300, labelfn=lambda k,v:k)
        d.add(Box(pie0a))

        legend0a = Legend(pie0a.getPalette(),300)
        d.add(legend0a)

        d.add(Text("Doughnut"))

        pie1 = Pie(data0, value=1,colour=0,width=400, height=400, colour_manager=colour_manager0, doughnut=True)
        d.add(Box(pie1))

        legend1 = Legend(colour_manager0,400,legend_columns=1)
        d.add(legend1)
        
        d.add(Text("Monochrome"))

        data2 = [("AAAA",1.2),("BBBB",0.4),("CCCC",0.9),("DDDD",0.9),("EEEE",1.0)]
        pie2 = Pie(data2, value=1,colour=0, width=400, height=400, labelfn = lambda k,v:k)
        d.add(Box(pie2))
    
        d.add(Text("Multi-level"))

        data3 = [
            ("A",10,""),
            ("B",15,"B.1"),
            ("B",5,"B.2"),
            ("C",4,""),
            ("D",12,"D.1"),
            ("D",3,"D.2"),
            ("D",5,"D.3")]

        pie3 = Pie(data3, value=1,colour=[0,2], width=600, height=600)
        d.add(Box(pie3))
        legend3 = Legend(pie3.getPalette(),400)
        d.add(legend3)
        d.connect(legend3,"colour",pie3,"colour")
        d.connect(pie3,"colour",legend3,"colour")

        d.add(Text("Multi-level Doughnut"))


        pie4 = Pie(data3, value=1,colour=[0,2], width=600, height=600, doughnut=True)
        d.add(Box(pie4))

        TestUtils.draw_output(d,"test_pie")
    
if __name__ == "__main__":
    unittest.main()
