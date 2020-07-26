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

import os

from visigoth.svg import polygon, circle, path, line, rectangle, clip_path, embedded_svg
from visigoth.map_layers.geoplot.multithing import Multithing

class Multiline(Multithing):

    """
    Create a set of one or more lines

    Arguments:
        coordinates (list): list of lists of (lon,lat) pairs specifying the location of points in a line
        
    Keyword Arguments:
        id (str): an ID associated with the polygon
        category (str): a category associated with the polygon
        label (str): a label associated with these lines
        tooltip (str): a tooltip associated with these lines
        popup (visigoth.containers.popup.Popup): a popup to display when the lines are clicked
        properties (dict): metadata for the lines
        fill (str): a fill colour to use
        stroke (stroke): the stroke colour to use
        stroke_width (float): the width of the stroke
    """
    def __init__(self,coordinates,id="",category="",label="",tooltip="",popup=None,properties={},fill="red",stroke="black",width=5,stroke_width=1):
        super(Multiline,self).__init__(id,category,label,tooltip,popup,properties,fill,stroke,stroke_width)
        self.coordinates = coordinates
        self.width=0
        
    def getCoordinates(self):
        return self.coordinates

    def draw(self,doc,points):
        kwargs = {}
        if self.tooltip:
            kwargs["tooltip"] = self.tooltip
        if self.width and self.fill and self.width>self.stroke_width:
            p2 = path(points,self.stroke,self.width+self.stroke_width,**kwargs)
            doc.add(p2)
            p1 = path(points,self.fill,self.width-self.stroke_width,**kwargs)
            doc.add(p1)
            return [(p1,self.width-self.stroke_width),(p2,self.width+self.stroke_width)]
        else:
            p = path(points,self.stroke,self.stroke_width,**kwargs)
            doc.add(p)
            return [(p,self.stroke_width)]
            
    