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
        TestUtils.draw_output(d,"test_embedded_svg")

if __name__ == "__main__":
    unittest.main()
