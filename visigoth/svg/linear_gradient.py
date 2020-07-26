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

from xml.dom.minidom import *
from math import cos,sin,pi
import json

from visigoth.svg.svgdefinition import svgdefinition

class linear_gradient(svgdefinition):

    counter = 0

    def __init__(self, startCol, stopCol, orientation="horizontal"):
        svgdefinition.__init__(self,"lg_"+str(linear_gradient.counter))
        linear_gradient.counter += 1
        self.startCol = startCol
        self.stopCol = stopCol
        self.orientation = orientation

    def render(self,svgdoc):
        doc = svgdoc.doc
        lg = doc.createElement("linearGradient")
        lg.setAttribute("id",self.getId())
        if self.orientation == "vertical":
            lg.setAttribute("x1","0")
            lg.setAttribute("x2","0")
            lg.setAttribute("y1","1")
            lg.setAttribute("y2","0")
        stop0 = doc.createElement("stop")
        stop0.setAttribute("offset","0%")
        stop0.setAttribute("stop-color",self.startCol)
        stop100 = doc.createElement("stop")
        stop100.setAttribute("offset", "100%")
        stop100.setAttribute("stop-color", self.stopCol)
        lg.appendChild(stop0)
        lg.appendChild(stop100)
        svgdoc.defs.appendChild(lg)
        return lg