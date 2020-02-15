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
