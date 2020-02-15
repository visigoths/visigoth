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
from visigoth.containers.box import Box
from visigoth.containers.grid import Grid
from visigoth.common.text import Text

class TestGrid(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        g = Grid()
        g.add(0,0,Box(Text("Top-Left Cell in Grid")))
        g.add(0,1,Box(Text("Right-Justified"),fill="orange").setRightJustified())
        g.add(1,0,Box(Text("Middle Left")))
        g.add(1,1,Box(Text("Middle Right")))
        g.add(2,0,Box(Text("Left-Justified"),fill="green").setLeftJustified())
        g.add(2,1,Box(Text("Bottom-Right Cell in Grid")))
        d.add(Box(g))

        sparse = Grid()
        sparse.add(0,0,Box(Text("Top Left")))
        sparse.add(10,10,Box(Text("Bottom Right")))
        d.add(Box(sparse))

        lined = Grid(stroke="grey",stroke_width=2)
        lined.add(0,0,Box(Text("Top Left")))
        lined.add(10,10,Box(Text("Bottom Right")))
        d.add(lined)

        grid_10_10 = Grid(stroke="grey",stroke_width=2)
        for x in range(10):
            for y in range(10):
                grid_10_10.add(x,y,Box(Text(str((x,y)),font_height=12)))
        d.add(grid_10_10)

        colourgrid = Grid(fill="yellow")
        colourgrid.add(0,0,Box(Text("Top Left")))
        colourgrid.add(10,10,Box(Text("Bottom Right")))
        d.add(Box(colourgrid))

        svg = d.draw()
        TestUtils.output(svg,"test_grid.svg")
