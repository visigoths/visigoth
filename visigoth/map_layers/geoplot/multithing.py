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

class Multithing(object):

    """
    Base class for an object (point,line,polygon)

    Arguments:
        id (str): an ID associated with the polygon
        category (str): a category associated with the polygon
        label (str): a label associated with these polygons
        tooltip (str): a tooltip associated with these polygons
        popup (visigoth.containers.popup.Popup): a popup to display when the polygons are clicked
        properties (dict): metadata for the polygons
        fill (str): a fill colour to use
        stroke (stroke): the stroke colour to use
        stroke_width (float): the width of the stroke
    """
    
    def __init__(self,id,category,label,tooltip,popup,properties,fill,stroke,stroke_width):
        self.id = id
        self.category = category
        self.label = label
        self.tooltip = tooltip
        self.popup = popup
        self.properties = properties
        self.fill = fill
        self.stroke = stroke 
        self.stroke_width = stroke_width

    def getCoordinates(self):
        return self.coordinates

    def getId(self):
        return self.id

    def getCategory(self):
        return self.category

    def getLabel(self):
        return self.label

    def getStrokeWidth(self):
        return self.stroke_width 

    def getPopup(self):
        return self.popup
    
    def getProperties(self):
        return self.properties
