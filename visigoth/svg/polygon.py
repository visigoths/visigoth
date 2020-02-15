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

from visigoth.svg.svgstyled import svgstyled

# represent a polygon as an SVG object
class polygon(svgstyled):

    def __init__(self,path,fill=None,stroke="black",stroke_width=1,tooltip="",innerpaths=[]):
        svgstyled.__init__(self,"path",tooltip)
        s = self.buildPath(path)

        if innerpaths:
            self.addAttr("fill-rule","evenodd")
            for path in innerpaths:
                s += " "
                s += self.buildPath(path)

        self.addAttr("d",s)

        if fill:
            self.addAttr("fill",fill)
        else:
            self.addAttr("fill","none")
        if stroke and stroke_width:
            self.addAttr("stroke-width",stroke_width).addAttr("stroke",stroke)



    def buildPath(self,points):
        s = 'M'
        sep = ''
        for p in points:
            if len(p) == 1:
                s += " "+p[0]
                continue
            (x,y) = p
            s += sep
            sep = ' '
            s += str(x)+" "+str(y)
        s += 'Z'
        return s