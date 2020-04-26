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
            
    