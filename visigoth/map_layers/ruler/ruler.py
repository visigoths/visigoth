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

import os.path

from visigoth.map_layers import MapLayer
from visigoth.svg import text, line
from visigoth.utils.js import Js
from visigoth.utils.mapping import Mapping

class Ruler(MapLayer):

    """
    Construct a map layer to display a ruler

    Keyword Arguments:
        label(str): label for ruler
        decimal_places(int): the number of decimal places to display
        stroke(str): stroke colour for axis line
        stroke_width(int): width of axis line
        font_height(int): the font size in pixels
        text_attributes(dict): a dict containing SVG name/value pairs
    """

    def __init__(self,label="",decimal_places=2,stroke="black",stroke_width=2,font_height=16,text_attributes={}):
        super(Ruler,self).__init__()
        self.length = 0
        self.ruler_width = font_height / 2
        self.distance = 0
        self.decimal_places = decimal_places
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.font_height = font_height
        self.text_attributes = text_attributes

    def isForegroundLayer(self):
        return True

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to,fmt):
        self.ownermap = ownermap
        self.width = width
        self.height = height
        self.boundaries = boundaries
        self.projection = projection

        min_lon = boundaries[0][0]
        max_lon = boundaries[1][0]
        mid_lat = (boundaries[0][1] + boundaries[1][1])/2

        dist = Mapping.haversine((min_lon,mid_lat),(max_lon,mid_lat))
        # compute the ruler based on distances along the vertical middle of the map
        # projection will mean that the ruler may be shorter or longer at the top/bottom

        self.height = height
        self.scale_x = self.width/dist

        half_distance = (0.5*width)/self.scale_x
        for ruler_distance in [20000000,10000000,5000000,2000000,1000000,500000,200000,100000,50000,20000,10000,5000,2000,1000,500,200,100,50,20,10,5,2,1]:
            if ruler_distance <= half_distance:
                break
        self.length = ruler_distance * self.scale_x
        self.distance = ruler_distance
        if self.distance >= 5000:
            self.distance = self.distance//1000
            self.units = "km"
        else:
            self.units = "m"
        self.label = str(self.distance)+self.units

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def draw(self,doc,cx,cy):
        ox = cx - self.width/2 + 20
        oy = cy + self.height/2 - 1.5*self.ruler_width

        lcx = ox + self.length/2

        l0 = line(lcx-self.length/2,oy+self.ruler_width/2,lcx+self.length/2,oy+self.ruler_width/2,stroke=self.stroke,stroke_width=self.stroke_width)
        l1 = line(lcx-self.length/2,oy-self.ruler_width/2,lcx-self.length/2,oy+self.ruler_width/2+self.stroke_width/2,stroke=self.stroke,stroke_width=self.stroke_width)
        l2 = line(lcx+self.length/2,oy-self.ruler_width/2,lcx+self.length/2,oy+self.ruler_width/2+self.stroke_width/2,stroke=self.stroke,stroke_width=self.stroke_width)
        doc.add(l0).add(l1).add(l2)

        t = text(ox+self.length+10,oy,self.label)
        t.addAttr("text-anchor","start")
        t.setVerticalCenter()
        t.addAttrs(self.text_attributes)
        t.addAttr("font-size",self.font_height)
        doc.add(t)

        with open(os.path.join(os.path.split(__file__)[0],"ruler.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = { "value":self.distance, "units":self.units, "label":t.getId() }
        Js.registerJs(doc,self,jscode,"ruler",cx,cy,config)
        