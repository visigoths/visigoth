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
from visigoth.map_layers.geoplot import Geoplot
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
        marker (bool): whether to draw a marker or circle
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

    