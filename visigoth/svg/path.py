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
from math import sqrt,atan2,cos,sin,pi
import json

from visigoth.svg.svgstyled import svgstyled
from visigoth.svg import circle

# represent a path as an SVG object
class path(svgstyled):

    def __init__(self,points,stroke,stroke_width,tooltip="",smoothing=None,fill=None,closed=False):
        svgstyled.__init__(self,"path",tooltip)
        self.smoothing = smoothing
        self.closed = closed
        if self.smoothing:
            s = self.computeSmoothedPath(points)
        else:
            s = self.computeStandardPath(points)
        self.addAttr("d",s)

        if fill == None:
            self.addAttr("fill","none")
        else:
            self.addAttr("fill",fill)
        if stroke and stroke_width:
            self.addAttr("stroke-width",stroke_width).addAttr("stroke",stroke)

    def close(self,points):
        path = self.getAttr("d")
        self.closed = True
        path += " "+self.computeStandardPath(points,action="L")
        self.addAttr("d",path)

    def computeLineLengthAngle(self,p0,p1):
        lX = p1[0] - p0[0]
        lY = p1[1] - p0[1]
        return (sqrt(lX**2 + lY**2),atan2(lY, lX))

    def computeCP(self,c,p,n,reverse,dist):
        if p == None:
            p = c
        if n == None:
            n = c

        lps = self.computeLineLengthAngle(p, n)

        angle = lps[1]
        if reverse:
            angle += pi
        l = min(lps[0],dist) * self.smoothing

        x = c[0] + cos(angle) * l
        y = c[1] + sin(angle) * l
        return (x,y)

    def computeSmoothedPath(self,points):
        s = ''
        for idx in range(len(points)):
            p = None
            pp = None
            n = None
            c = points[idx]
            if idx == 0:
                s += "M "
                s += str(c[0]) + "," + str(c[1])
            else:
                p = points[idx-1]
                if idx > 1:
                    pp = points[idx-2]
                elif self.closed:
                    pp = points[-2]
                if idx < len(points)-1:
                    n = points[idx+1]
                elif self.closed:
                    n = points[1]
                dist = self.computeLineLengthAngle(p,c)[0]
                cp0 = self.computeCP(p,pp,c,False,dist)
                cp1 = self.computeCP(c,p,n,True,dist)
                s += " C"
                s += " "+str(cp0[0])+","+str(cp0[1])
                s += " "+str(cp1[0])+","+str(cp1[1])
                s += " "+str(c[0])+","+str(c[1])
        if self.closed:
            s += " Z"
        return s

    def computeStandardPath(self,points,action='M'):
        sep = ''
        s = ''
        for p in points:
            s += action
            if len(p) == 1:
                s += " "+p[0]
                continue
            (x,y) = p
            s += sep
            sep = ' '
            s += str(x)+" "+str(y)
            action = "L"
        if self.closed:
            s += " Z"
        return s

