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