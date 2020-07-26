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


import math
import os.path

from visigoth.svg import circle, text, path
from visigoth.map_layers import MapLayer
from visigoth.utils.term.progress import Progress
from visigoth.utils.js import Js

class Compass(MapLayer):

    """
    Create a compass layer showing the user device heading (if available on the user device)

    Arguments:
        
    Keyword Arguments:
        radius (int): radius of compass in pixels
        fill(str): fill colour
        stroke (str): stroke color for circumference of compass and text
        stroke_width (int): stroke width for circumference of compass
        
    Notes:

    """

    def __init__(self, radius=40, fill="lightgrey", stroke="black", stroke_width=2):
        super(Compass, self).__init__()
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
        self.height = height
        self.zoom_to = zoom_to
        
    def getBoundaries(self):
        return self.boundaries

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def isForegroundLayer(self):
        return True

    def build(self,fmt):
        pass
        
    def draw(self,doc,cx,cy):
        x = cx + self.width/2 - self.radius - 10
        y = cy - self.height/2 + self.radius + 10

        c = circle(x, y, self.radius, fill=self.fill, stroke=self.stroke, stroke_width=self.stroke_width)
        doc.add(c)

        for (s,angle) in [("N",0.0),("E",math.pi*0.5),("S",math.pi),("W",math.pi*1.5)]:
            tx = x + self.radius*0.8*math.sin(angle)
            ty = y - self.radius*0.8*math.cos(angle)
            t = text(tx,ty,s,font_height=self.radius*0.3)
            t.setHorizontalCenter()
            t.setVerticalCenter()
            doc.add(t)
        
        needle_width = self.radius/4
        needleg = doc.openGroup()
        needleg.addAttr("visibility","hidden");
        p1 = path([(x-needle_width/2,y),(x+needle_width/2,y),(x,y-self.radius*0.65)],"black",1,fill="red")
        p2 = path([(x-needle_width/2,y),(x+needle_width/2,y),(x,y+self.radius*0.65)],"black",1,fill="white")
        doc.add(p1).add(p2)
        doc.closeGroup()

        dot = circle(x,y,needle_width/3,fill="black")
        doc.add(dot)

        with open(os.path.join(os.path.split(__file__)[0], "compass.js"), "r") as jsfile:
            jscode = jsfile.read()

        config = { "x":x, "y":y, "needle":needleg.getId() }
        Js.registerJs(doc, self, jscode, "compass", cx, cy, config)

        
