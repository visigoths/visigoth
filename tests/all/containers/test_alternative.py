# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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
from visigoth.containers import Alternative, Box
from visigoth.common import Button, ButtonGrid, Text

class TestAlternative(unittest.TestCase):

    def test_basic(self):

        d = Diagram(fill="white")

        text1 = Text("This is text 1")
        text2 = Text("This is text 2")

        a = Alternative()
        a.add(text1)
        a.add(text2)

        b1 = Button(text="Show text 1",click_value=text1.getId())
        b2 = Button(text="Show text 2",click_value=text2.getId())

        bg = ButtonGrid()
        bg.addButton(0,0,b1,initially_selected=True)
        bg.addButton(0,1,b2)

        d.add(bg)

        d.add(Box(a,fill="lightgrey"))
        d.connect(bg,"click",a,"show")

        TestUtils.draw_output(d,"test_alternative")

if __name__ == "__main__":
    unittest.main()
