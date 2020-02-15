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
from visigoth.containers.sequence import Sequence
from visigoth.common.text import Text
from visigoth.common.space import Space

class TestSequence(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        s = Sequence()
        s.add(Space(0,400))
        s.add(Box(Text("First")))
        s.add(Box(Text("Right-Justified"),fill="orange").setRightJustified())
        s.add(Box(Text("Middle")))
        s.add(Box(Text("Left-Justified"),fill="green").setLeftJustified())
        s.add(Box(Text("Last")))
        d.add(Box(s))


        s = Sequence(orientation="hotizontal")
        s.add(Box(Text("First"),fill="orange"))
        s.add(Box(Text("Second"),fill="lightblue"))
        s.add(Box(Text("Third"),fill="lightgreen"))
        d.add(Box(s))

        svg = d.draw()
        TestUtils.output(svg, "test_sequence.svg")