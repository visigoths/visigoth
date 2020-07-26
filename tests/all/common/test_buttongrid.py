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
from visigoth.common import Button, ButtonGrid

class TestButton(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        bg = ButtonGrid()
        bg.addButton(0,0,Button("Button(row=0,col=0)"),True)
        bg.addButton(0,1,Button("Button(row=0,col=1)"))
        bg.addButton(0,2,Button("Button(row=0,col=2)"))
        bg.addButton(1,0,Button("Button(row=1,col=0)"))
        bg.addButton(1,1,Button("Button(row=1,col=1)"))
        bg.addButton(1,2,Button("Button(row=1,col=2)"))

        TestUtils.draw_output(d,"test_buttongrid")

if __name__ == "__main__":
    unittest.main()
