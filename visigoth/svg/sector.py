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