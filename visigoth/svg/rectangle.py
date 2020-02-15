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

# represent a rectangle as an SVG object
class rectangle(svgstyled):

    def __init__(self,x,y,width,height,fill=None,stroke=None,stroke_width=None,rx=None, ry=None, tooltip=""):
        svgstyled.__init__(self,"rect",tooltip)
        self.addAttr("x",x)
        self.addAttr("y",y)
        self.addAttr("width",width)
        self.addAttr("height",height)
        if fill:
            self.addAttr("fill",fill)
        else:
            self.addAttr("fill","none")
        if stroke:
            self.addAttr("stroke",stroke)
        if stroke_width:
            self.addAttr("stroke-width",stroke_width)
        if rx:
            self.addAttr("rx",rx)
        if ry:
            self.addAttr("ry",ry)
