# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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