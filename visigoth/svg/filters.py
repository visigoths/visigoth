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

from xml.dom.minidom import *
from math import cos,sin,pi
import json

from visigoth.svg.svgdefinition import svgdefinition


class glow(svgdefinition):

    def __init__(self):
        svgdefinition.__init__(self,"glow")

    def render(self,svgdoc):
        f= svgdoc.doc.createElement("filter")
        f.setAttribute("id",self.getId())

        f.setAttribute("width","1.5")
        f.setAttribute("height","1.5")
        f.setAttribute("x","-0.25")
        f.setAttribute("y","-0.25")
        
        flood = svgdoc.doc.createElement("feFlood")
        flood.setAttribute("id","outline-color")
        flood.setAttribute("flood-color","orange")
        flood.setAttribute("result","base")

        morph = svgdoc.doc.createElement("feMorphology")
        morph.setAttribute("result","bigger")
        morph.setAttribute("in","SourceGraphic")
        morph.setAttribute("operator","dilate")
        morph.setAttribute("radius","5")

        cm = svgdoc.doc.createElement("feColorMatrix")
        cm.setAttribute("type","matrix")
        cm.setAttribute("result","mask") 
        cm.setAttribute("in","bigger")
        cm.setAttribute("values","0 0 0 0 0 "+"0 0 0 0 0 "+"0 0 0 0 0 "+"0 0 0 1 0")

        comp = svgdoc.doc.createElement("feComposite")
        comp.setAttribute("result","drop")
        comp.setAttribute("in","base") 
        comp.setAttribute("in2","mask") 
        comp.setAttribute("operator","in") 

        #  bl = svgdoc.doc.createElement("feGaussianBlur")
        # bl.setAttribute("result","blurred")
        # bl.setAttribute("in","drop")
        # bl.setAttribute("stdDeviation","5")
        
        mg = svgdoc.doc.createElement("feBlend")
        mg.setAttribute("in","SourceGraphic")
        mg.setAttribute("in2","drop")
        mg.setAttribute("mode","normal")

        f.appendChild(flood)
        f.appendChild(morph)
        f.appendChild(cm)
        f.appendChild(comp)
        # f.appendChild(bl)
        f.appendChild(mg)
        svgdoc.defs.appendChild(f)