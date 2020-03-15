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
            area0 = Area([d for d in data if d[2] == cat],x=0,y=1,palette=dp,height=300,width=300)
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
        d.connect(legend1,"brushing",area1,"brushing")
        d.connect(area1,"brushing",legend1,"brushing")
        
        for smoothing in [0.1,0.3,0.5]:
            d.add(Text("Smoothing=%f"%(smoothing)))
            area2 = Area(data, x=0, y=1, colour=2, height=400, smoothing=smoothing, palette=dp, width=400)
            d.add(area2)

        
        svg = d.draw()
        TestUtils.output(svg,"test_area.svg")

if __name__ == "__main__":
    unittest.main()