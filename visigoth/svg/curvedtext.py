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

from visigoth.svg.svgstyled import svgstyled

class curvedtext(svgstyled):

    counter = 0

    def __init__(self, ox, oy, r, text, tooltip=""):
        self.id = "ct"+str(curvedtext.counter)
        curvedtext.counter += 1
        svgstyled.__init__(self, "text", tooltip)
        theta1 = 0
        theta2 = pi
        self.path = "M" + str(ox + -r * cos(theta1)) + "," + str(oy + r * -sin(theta1)) + " "
        self.path += "A" + str(r) + "," + str(r) + "," + "0,0,1," + str(ox + -r * cos(theta2)) + "," + str(
            oy + -r * sin(theta2)) + " "
        self.text = text
        self.addAttr("alignment-baseline","baseline")
        self.addAttr("text-anchor","middle")

    def render(self,svgdoc,parent):
        t = super(curvedtext,self).render(svgdoc,parent)
        doc = svgdoc.doc
        p = doc.createElement("path")
        p.setAttribute("id",self.id)
        p.setAttribute("d",self.path)
        svgdoc.defs.appendChild(p)
        tp = doc.createElement("textPath")
        tp.setAttribute("xlink:href","#"+self.id)
        tp.setAttribute("startOffset","50%")
        t.appendChild(tp)
        tp.appendChild(doc.createTextNode(self.text))
        return tp