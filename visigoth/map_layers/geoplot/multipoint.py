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

class Multipoint(Multithing):

    location_marker=open(os.path.join(os.path.split(__file__)[0],"location_ionicon.svg"),"rt").read()
    
    """
    Create a set of one or more points

    Arguments:
        coordinates (list): list of (lon,lat) pairs specifying the location of each point
        
    Keyword Arguments:
        id (str): an ID associated with the polygon
        category (str): a category associated with the polygon
        label (str): a label associated with these points
        tooltip (str): a tooltip associated with these points
        popup (visigoth.containers.popup.Popup): a popup to display when the points are clicked
        properties (dict): metadata for the points
        fill (str): a fill colour to use
        stroke (stroke): the stroke colour to use
        stroke_width (float): the width of the stroke
        radius (int): the radius of the point
        marker (bool|Marker): whether to draw a marker or circle (bool) or a marker object
    """

    def __init__(self,coordinates,id="",category="",label="",tooltip="",popup=None,properties={},fill="red",stroke="black",stroke_width=1,radius=20,marker=True):
        super(Multipoint,self).__init__(id,category,label,tooltip,popup,properties,fill,stroke,stroke_width)
        self.coordinates = coordinates
        self.radius = radius
        self.marker = marker

    def getCoordinates(self):
        return self.coordinates

    def getRadius(self):
        return self.radius

    def getMarker(self):
        return self.marker

    def draw(self,doc,xy):
        if isinstance(self.marker,bool):
            if self.marker:
                off_y = 32*(2*self.radius/512)
                i = embedded_svg(2*self.radius,2*self.radius,xy[0]-self.radius,xy[1]-2*self.radius+off_y,Multipoint.location_marker)
                i.addAttr("fill",self.fill)
                i.addAttr("stroke",self.stroke)
                i.addAttr("stroke-width",self.stroke_width)
                if self.tooltip:
                    i.setTooltip(self.tooltip)
                doc.add(i)
                return i.getId()
            else:
                c = circle(xy[0],xy[1],self.radius,self.fill)
                c.addAttr("stroke",self.stroke)
                c.addAttr("stroke-width",self.stroke_width)
                if self.tooltip:
                    c.setTooltip(self.tooltip)
                doc.add(c)
                return c.getId()
        else:
            return self.marker.plot(doc,xy[0],xy[1],self.tooltip,self.fill)
    