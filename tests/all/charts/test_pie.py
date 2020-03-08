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
from visigoth.charts.pie import Pie
from visigoth.utils.colour import DiscretePalette
from visigoth.common import Legend, Text
from visigoth.containers import Box

class TestPie(unittest.TestCase):

    def test_page(self):
        d = Diagram(fill="white")

        d.add(Text("Basic"))
        palette0 = DiscretePalette()
        palette0.addCategory("category A","#E7FFAC").addCategory("category B","#FFC9DE")
        palette0.addCategory("category C","#B28DFF").addCategory("category D","#ACE7FF")

        data0 = [("category A",1.2),("category B",0.1),("category C",0.4),("category D",0.5)]
        pie0 = Pie(data0, value=1,colour=0, width=400, height=400, palette=palette0)
        d.add(Box(pie0))

        legend0 = Legend(palette0,400,legend_columns=1)
        d.add(legend0)

        d.add(Text("Basic (Count)"))
        
        data0a = [("Cars",),("Cars",),("Cars",),("Bikes",),("Bikes",),("Trucks",),("Bikes",),("Bikes",)]
        pie0a = Pie(data0a, colour=0, width=300, height=300, labelfn=lambda k,v:k)
        d.add(Box(pie0a))

        legend0a = Legend(pie0a.getPalette(),300)
        d.add(legend0a)

        d.add(Text("Doughnut"))

        pie1 = Pie(data0, value=1,colour=0,width=400, height=400, palette=palette0, doughnut=True)
        d.add(Box(pie1))

        legend1 = Legend(palette0,400,legend_columns=1)
        d.add(legend1)
        
        d.add(Text("Monochrome"))

        data2 = [("AAAA",1.2),("BBBB",0.4),("CCCC",0.9),("DDDD",0.9),("EEEE",1.0)]
        pie2 = Pie(data2, value=1,colour=0, width=400, height=400, labelfn = lambda k,v:k)
        pie2.setPalette(None)
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
        d.connect(legend3,"brushing",pie3,"brushing")
        d.connect(pie3,"brushing",legend3,"brushing")

        d.add(Text("Multi-level Doughnut"))


        pie4 = Pie(data3, value=1,colour=[0,2], width=600, height=600, doughnut=True)
        d.add(Box(pie4))
        
        svg = d.draw()
        TestUtils.output(svg,"test_pie.svg")
    
if __name__ == "__main__":
    unittest.main()
