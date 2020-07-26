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

        TestUtils.draw_output(d,"test_grid")

if __name__ == "__main__":
    unittest.main()
