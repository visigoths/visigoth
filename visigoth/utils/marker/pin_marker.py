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

import os.path
from visigoth.svg import embedded_svg
from .marker import Marker

class PinMarker(Marker):

    svg = open(os.path.join(os.path.split(__file__)[0], "location_ionicon.svg"), "rt").read()

    def __init__(self, radius, stroke, stroke_width):
        super().__init__(radius,stroke,stroke_width)

    def plot(self, doc, x, y, tooltip, colour):
        r = self.getRadius()
        off_y = 32 * (2 * r / 512)
        i = embedded_svg(2 * r, 2 * r, x - r, y - 2 * r + off_y, PinMarker.svg)
        i.addAttr("fill", colour)
        i.addAttr("stroke", self.getStroke())
        i.addAttr("stroke-width", self.getStrokeWidth())
        if tooltip:
            i.setTooltip(tooltip)
        doc.add(i)
        return i.getId()


