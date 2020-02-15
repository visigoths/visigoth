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
from visigoth.containers.popup import Popup
from visigoth.common.text import Text

class TestPopup(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        p0 = Popup(Text("Popup Content"),"TEST")
        d.add(p0)

        p1 = Popup(Text("Orange Border"),"TEST",stroke="orange")
        d.add(p1)

        p2 = Popup(Text("Light Blue Fill"),"TEST",fill="lightblue")
        d.add(p2)

        p3 = Popup(Text("Thick Border"),"TEST",stroke_width=5)
        d.add(p3)

        p4 = Popup(Text("Light Blue Fill"),"Large Font",font_height=24,fill="lightblue")
        d.add(p4)

        p5 = Popup(Text("Reduced Opacity"),"TEST",fill="orange",opacity=0.2)
        d.add(p5)

        svg = d.draw()
        TestUtils.output(svg,"test_popup.svg")


