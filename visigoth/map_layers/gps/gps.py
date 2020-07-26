# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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


from math import sqrt
import copy
import os.path
import random

from visigoth.svg import circle, line
from visigoth.map_layers import MapLayer
from visigoth.utils.term.progress import Progress
from visigoth.utils.js import Js

class GPS(MapLayer):

    """
    Create a plot showing the user location (if known) with a pulsating circle

    Arguments:
        
    Keyword Arguments:
        radius (int): radius of circle in pixels
        fill(str): fill colour
        stroke (str): stroke color for circumference of circles
        stroke_width (int): stroke width for circumference of circles
        
    Notes:

    """

    def __init__(self, radius=20, fill="#FF000030", stroke="black", stroke_width=2):
        super(GPS, self).__init__()
        self.width = None
        self.height = None
        self.radius = radius
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        
    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to,fmt):
        self.width = width
        self.boundaries = boundaries
        self.projection = projection
        (self.x0,self.y0) = projection.fromLonLat(boundaries[0])
        (self.x1,self.y1) = projection.fromLonLat(boundaries[1])
        self.height = height
        self.scale_x = self.width/(self.x1-self.x0)
        self.scale_y = self.height/(self.y1-self.y0)
        self.zoom_to = zoom_to
        
    def getBoundaries(self):
        return self.boundaries

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def build(self,fmt):
        pass
        
    def draw(self,svgdoc,cx,cy):

        ox = cx - self.width/2
        oy = cy - self.height/2

        x = ox+((self.x1-self.x0)/2)*self.scale_x
        y = oy+((self.y1-self.y0)/2)*self.scale_y

        c = circle(ox, oy, self.radius, fill=self.fill, stroke=self.stroke, stroke_width=self.stroke_width)
        # c.addAttr("visibility","hidden")
        c.addAnimation("r",self.radius/2,self.radius,1)
        c.addAnimation("opacity",1.0,0.0,1)
        marker_id = c.getId()
        svgdoc.add(c)
        
        with open(os.path.join(os.path.split(__file__)[0], "gps.js"), "r") as jsfile:
            jscode = jsfile.read()

        lon_min = self.boundaries[0][0]
        lat_min = self.boundaries[0][1]
        lon_max = self.boundaries[1][0]
        lat_max = self.boundaries[1][1]

        config = { "marker_id":marker_id, "lon_min":lon_min, "lon_max":lon_max, "lat_min":lat_min, "lat_max":lat_max }
        Js.registerJs(svgdoc, self, jscode, "gps", cx, cy, config)

        
