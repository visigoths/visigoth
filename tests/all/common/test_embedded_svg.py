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
from visigoth.common.embedded_svg import EmbeddedSvg

svg = """<?xml version="1.0" encoding="utf-8"?>
<svg height="32" version="1.1" width="32" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <circle r="12" cx="16" cy="16" fill="%s" stroke="purple" stroke-width="2" />
</svg>
"""

svg_red = svg%("red")
svg_blue = svg%("blue")

class TestEmbeddedSvg(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")
        d.add(Box(EmbeddedSvg(svg_red,width=64,height=64)))
        d.add(Space(20))
        d.add(Box(EmbeddedSvg(svg_blue,width=32,height=32)))
        svg = d.draw()
        TestUtils.output(svg,"test_embedded_svg.svg")

if __name__ == "__main__":
    unittest.main()
