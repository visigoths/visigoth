# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

from visigoth.svg.svgstyled import svgstyled

# represent a line with a cubic bezier curve as an SVG object
class cubic_bezier(svgstyled):

    def __init__(self,p1,cp1,cp2,p2,stroke,stroke_width,tooltip=""):
        svgstyled.__init__(self,"path",tooltip)
        self.addAttr("d",self.computePath(p1,cp1,cp2,p2))
        self.addAttr("fill","none")
        if stroke and stroke_width:
            self.addAttr("stroke-width",stroke_width).addAttr("stroke",stroke)

    def addPoint(self,p):
        return str(p[0]) + "," + str(p[1])

    def computePath(self,p1,cp1,cp2,p2):
        s = "M"+self.addPoint(p1)
        s += " C"+self.addPoint(cp1)
        s += " "+self.addPoint(cp2)
        s += " "+self.addPoint(p2)
        return s

