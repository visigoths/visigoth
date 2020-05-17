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
        
        data1 = [("A",10,"A"),("B",25,"B"),("C",-4,"C"),("D",-5,"D1"),("D",-2,"D2")]

        bar1 = Bar(data1,x=0,y=1,colour=2,width=400, height=400, palette=palette1,labelfn=lambda k,v:"%d"%v)
        d.add(bar1)
        legend1 = Legend(palette1,400,legend_columns=2)
        d.add(legend1)
        d.connect(legend1,"colour",bar1,"colour")
        d.connect(bar1,"colour",legend1,"colour")
        svg = d.draw()
        TestUtils.output(svg,"test_bar.svg")

    def test_nopalette(self):
        d = Diagram(fill="white")
        data = [("A",10),("B",5),("C",-4),("D",-25)]
        bar = Bar(data,x=0,y=1,width=400,height=400,labelfn=lambda k,v:"%d"%v)
        d.add(bar)
        svg = d.draw()
        TestUtils.output(svg,"test_bar_nopalette.svg")

if __name__ == "__main__":
    unittest.main()