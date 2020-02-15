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