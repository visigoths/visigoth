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

from visigoth.diagram import Diagram
from visigoth.charts.transition import Transition
from visigoth.utils.colour import DiscretePalette
from visigoth.common.space import Space
from visigoth.common.legend import Legend
from visigoth.common.text import Text

from visigoth.utils.test_utils import TestUtils

class TestTransition(unittest.TestCase):

    def test_basic(self):

        palette = DiscretePalette()
        palette.addColour("A", "green").addColour("B", "blue").addColour("C", "red").addColour("D","orange")

        data = [
            ["S0", "","","A","A","A"],
            ["S1", "A","A","A","B","B"],
            ["S2", "A","A","B","C","C"],
            ["S3", "A","B","C","C","D"],
            ["S4", "A","B","C","D",""]
        ]

        d = Diagram(fill="white")

        d.add(Text("Basic Test",font_height=32,text_attributes={"stroke":"red"}))
        t = Transition(data,width=1024,height=512,palette=palette,transition_labels=["T1", "T2","T3","T4","T5"],y_axis_label="Count")
        d.add(t)
        d.add(Space(20,20))
        l = Legend(palette,1024, legend_columns=4)
        d.add(l)

        d.connect(t,"colour",l,"colour")
        d.connect(l,"colour",t,"colour")

        TestUtils.draw_output(d,"test_transition")

if __name__ == "__main__":
    unittest.main()