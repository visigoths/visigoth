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

from visigoth.utils.marker.circle_marker import CircleMarker
from visigoth.utils.marker.pin_marker import PinMarker

class MarkerManager(object):

    def __init__(self,min_radius=1,max_radius=10,default_radius=3,stroke="black",stroke_width=1):
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.size_min = None
        self.size_max = None
        self.default_radius = default_radius
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.marker_type = "circle"

    def setDefaultRadius(self,default_radius):
        self.default_radius = default_radius
        return self

    def getDefaultRadius(self):
        return self.default_radius

    def getStroke(self):
        return self.stroke

    def getStrokeWidth(self):
        return self.stroke_width

    def noteSize(self,size):
        if self.size_min is None or size < self.size_min:
            self.size_min = size
        if self.size_max is None or size > self.size_max:
            self.size_max = size

    def setMarkerType(self,marker_type):
        self.marker_type = marker_type
        return self

    def getRadius(self,size=None):
        if size is None or self.size_max is None:
            return self.default_radius
        else:
            return self.min_radius + (self.max_radius - self.min_radius) * (size / self.size_max)

    def getMarker(self,size=None):
        r = self.getRadius(size)
        if self.marker_type == "circle":
            return CircleMarker(r,self.stroke,self.stroke_width)
        if self.marker_type == "pin":
            return PinMarker(r,self.stroke,self.stroke_width)
        raise Exception("Unknown marker type: %s"%(self.marker_type))

    def getCircleMarker(self,radius):
        return CircleMarker(radius, self.stroke, self.stroke_width)