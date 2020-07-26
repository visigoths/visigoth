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

import json
from math import pi, floor, log10, ceil

from visigoth.common.diagram_element import DiagramElement
from visigoth.svg import text, line

class Ruler(DiagramElement):

    """
    Construct a ruler to represent a given distance on a map

    Arguments:
        length(int): length of the ruler in pixels
        ruler_width(int): width of the ruler in pixels
        distance(numeric): length of the ruler in meters

    Keyword Arguments:
        decimal_places(int): the number of decimal places to display
        stroke(str): stroke colour for axis line
        stroke_width(int): width of axis line
        font_height(int): the font size in pixels
        text_attributes(dict): a dict containing SVG name/value pairs
    """

    def __init__(self,length,distance,ruler_width=10,decimal_places=2,stroke="black",stroke_width=4,font_height=24,text_attributes={}):
        DiagramElement.__init__(self)
        self.length = length
        self.ruler_width = ruler_width
        self.distance = distance
        if self.distance >= 5000:
            self.distance = self.distance//1000
            self.units = "km"
        else:
            self.units = "m"
        self.decimal_places = decimal_places
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.label = str(self.distance)+self.units

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setStroke(self,stroke,stroke_width):
        """
        Configure ruler colour and width

        Arguments:
           stroke(str): stroke colour for axis line
            stroke_width(int): width of axis line
        """
        self.stroke = stroke
        self.stroke_width = stroke_width


    def build(self,fmt):
        self.width = self.length+2*len(self.label)*self.font_height
        self.height = max(self.ruler_width,self.font_height)

    def draw(self,doc,cx,cy):
        ox = cx - self.width/2
        oy = cy - self.height/2

        lcx = ox + self.length/2

        l0 = line(lcx-self.length/2,cy+self.ruler_width/2,lcx+self.length/2,cy+self.ruler_width/2,stroke=self.stroke,stroke_width=self.stroke_width)
        l1 = line(lcx-self.length/2,cy-self.ruler_width/2,lcx-self.length/2,cy+self.ruler_width/2+self.stroke_width/2,stroke=self.stroke,stroke_width=self.stroke_width)
        l2 = line(lcx+self.length/2,cy-self.ruler_width/2,lcx+self.length/2,cy+self.ruler_width/2+self.stroke_width/2,stroke=self.stroke,stroke_width=self.stroke_width)
        doc.add(l0).add(l1).add(l2)

        t = text(cx+self.length/2,cy,self.label)
        t.addAttr("dominant-baseline","middle")
        t.addAttrs(self.text_attributes)
        t.addAttr("font-size",self.font_height)
        doc.add(t)
