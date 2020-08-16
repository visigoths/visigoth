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


# represent a section of text as an SVG tspan object
class tspan(svgstyled):

    def __init__(self,txt,tooltip="",font_height=None,text_attributes={}):
        svgstyled.__init__(self,"tspan",tooltip)
        self.setContent(txt)
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.url = None

    def setUrl(self,url):
        self.url = url

    def render(self,svgdoc,parent):
        dattrs = svgdoc.getDiagram().getDefaultTextAttributes()
        self.addAttrs(dattrs)

        if self.text_attributes:
            self.addAttrs(self.text_attributes)

        if self.font_height:
            self.addAttr("font-size",self.font_height)

        font_family = self.text_attributes.get("font-family",dattrs.get("font-family",""))
        font_weight = self.text_attributes.get("font-weight",dattrs.get("font-weight","normal"))
        font_style = self.text_attributes.get("font-style",dattrs.get("font-style","normal"))

        svgdoc.includeFont(font_family,font_weight,font_style)

        if self.url:
            doc = svgdoc.doc
            self.addAttr("text-decoration","underline")
            self.addAttr("stroke", "blue")
            p = doc.createElement("a")
            parent.appendChild(p)
            p.setAttribute("href",self.url)
            p.setAttribute("target","_new")
            parent = p

        return super().render(svgdoc, parent)
