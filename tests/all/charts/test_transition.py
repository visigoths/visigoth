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
        palette.addCategory("A", "green").addCategory("B", "blue").addCategory("C", "red").addCategory("D","orange")

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

        d.connect(t,"brushing",l,"brushing")
        d.connect(l,"brushing",t,"brushing")

        svg = d.draw()
        TestUtils.output(svg,"test_transition.svg")

if __name__ == "__main__":
    unittest.main()