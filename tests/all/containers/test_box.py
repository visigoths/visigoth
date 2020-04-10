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
from visigoth.common.text import Text

class TestBox(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")
        d.add(Box(Text("Box")))
        d.add(Box(Text("Red Border"),stroke="red"))
        d.add(Box(Text("Thick Border"),stroke_width=10))
        d.add(Box(Text("Orange Box"),fill="orange"))
        d.add(Box(Text("Extra Padding"),padding=40))
        d.add(Box(Text("Extra Margin"),margin=40))
        d.add(Box(Text("Green Box, No Border"),fill="lightgreen",stroke_width=0))

        svg = d.draw()
        TestUtils.output(svg,"test_box.svg")

if __name__ == "__main__":
    unittest.main()
