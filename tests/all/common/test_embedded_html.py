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
from visigoth.common.space import Space
from visigoth.common.embedded_html import EmbeddedHtml

html_red = """<div style="color:red">Hello World!</div>"""
html_blue = """<div style="scroll:both;color:blue"><ul><li>Hello World!</li><li>Hello World!</li></ul></div>"""

class TestEmbeddedHtml(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")
        d.add(Box(EmbeddedHtml(html_red,"",width=256,height=32)))
        d.add(Space(20))
        d.add(Box(EmbeddedHtml(html_blue,"",width=256,height=32)))
        svg = d.draw()
        TestUtils.output(svg,"test_embedded_html.svg")

if __name__ == "__main__":
    unittest.main()
