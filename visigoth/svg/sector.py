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

class sector(svgstyled):

    def __init__(self,ox,oy,r1,r2,theta1,theta2,tooltip="",fill=None,stroke=None,stroke_width=None):
        svgstyled.__init__(self,"path",tooltip)
        s = "M"+str(ox+-r2*cos(theta1))+","+str(oy+r2*-sin(theta1))+" "
        x = 0
        if (theta2-theta1) > pi:
            x = 1
        s += "A"+str(r2)+","+str(r2)+","+"0,"+str(x)+",1,"+str(ox+-r2*cos(theta2))+","+str(oy+-r2*sin(theta2))+" "
        s += "L"+str(ox+-r1*cos(theta2))+","+str(oy+-r1*sin(theta2))+" "
        if r1:
            s += "A"+str(r1)+","+str(r1)+","+"0,"+str(x)+",0,"+str(ox+-r1*cos(theta1))+","+str(oy+-r1*sin(theta1))+" "
        s += "z"
        self.addAttr("d",s)
        if fill:
            self.addAttr("fill",fill)
        if stroke:
            self.addAttr("stroke",stroke)
        if stroke_width:
            self.addAttr("stroke-width",stroke_width)