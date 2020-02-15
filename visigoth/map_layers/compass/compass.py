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
        
    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
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

    def build(self):
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

        
