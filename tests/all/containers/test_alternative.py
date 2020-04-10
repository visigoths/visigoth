# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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
        svg = d.draw()

        TestUtils.output(svg,"test_alternative.svg")

if __name__ == "__main__":
    unittest.main()
