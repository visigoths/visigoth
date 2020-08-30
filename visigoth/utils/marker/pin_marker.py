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
from visigoth.svg import path
from .marker import Marker

class PinMarker(Marker):


    raw_path = [
        ("M",[(256,32)],""), # M256 32
        ("c",[(-88.004,0),(-160,70.557),(-160,156.801)],""), # c-88.004 0-160 70.557-160 156.801
        ("C",[(96,306.4),(256,480),(256,480)],""), # C96 306.4 256 480 256 480
        ("s",[(160,-173.6),(160,-291.199)],""), # s160-173.6 160-291.199
        ("C",[(416,102.557),(344.004,32),(256,32)],"z"), # C416 102.557 344.004 32 256 32z
        ("m",[(0,212.801)],""), # m0 212.801
        ("c",[(-31.996,0),(-57.144,-24.645),(-57.144,-56),(0,-31.357),(25.147,-56),(57.144,-56)],""), # c-31.996 0-57.144-24.645-57.144-56 0-31.357 25.147-56 57.144-56
        ("s",[(57.144,24.643),(57.144,56)],""), # s57.144 24.643 57.144 56
        ("c",[(0,31.355),(-25.148,56),(-57.144,56)],"") # c0 31.355-25.148 56-57.144 56
    ]

    def __init__(self, radius, stroke, stroke_width):
        super().__init__(radius,stroke,stroke_width)

    def plot(self, doc, x, y, tooltip, colour, visible=True):
        r = self.getRadius()
        scale = r/256
        off_x = -1 * x * (scale - 1)
        off_y = -1 * y * (scale - 1)
        p = path(fill=colour,stroke=self.getStroke(),stroke_width=self.getStrokeWidth(),closed=True)
        p.setRawPath(PinMarker.raw_path,off_x,off_y,scale)
        if tooltip:
            p.setTooltip(tooltip)
        p.addAttr("visibility", "visible" if visible else "hidden")
        doc.add(p)
        return p.getId()


