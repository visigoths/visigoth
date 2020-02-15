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


import random
import sys
import json
import copy
import os.path

from math import radians,sin,cos,pi,sqrt,log

from visigoth.svg import polygon
from visigoth.common import DiagramElement
from visigoth.map_layers.geoimport import Geoimport
from visigoth.utils.colour import Colour
from visigoth.map_layers import MapLayer
from visigoth.utils.js import Js


class Chloropleth(MapLayer):

    """
    Create a Choloropleth plot

    Arguments:
        path : a geojson or geopackage file path
        valuePropertyName(str) : the name of the property to provide the value to visualize
        labelPropertyName(str) : the name of the property to provide the label
        palette(list) : a list of (value, colour) pairs or a list of [(min-value, min-colour),(max-value,max-colour)]

    Keyword Arguments:
        default_fill_colour (str): default colour for areas where a value cannot be obtained
        stroke (str): stroke color for circumference of circles
        stroke_width (int): stroke width for circumference of circles

    Notes:

    """

    def __init__(self, path, valuePropertyName, labelPropertyName, palette, default_fill_colour="white", stroke="black",stroke_width=2):
        super(Chloropleth, self).__init__()
        self.path = path
        self.value = valuePropertyName
        self.labelPropertyName = labelPropertyName
        self.boundaries = None
        self.width = None
        self.height = None
        self.projection = None
        self.stroke = stroke
        self.palette = palette
        self.default_fill_colour = default_fill_colour
        self.stroke_width = stroke_width
        self.ownermap = None
        self.geojson = Geoimport(self.path,polygon_style=lambda props:self.getPolygonStyle(props))

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
        self.width = width
        self.height = height
        self.ownermap = ownermap
        self.boundaries = boundaries
        self.projection = projection
        self.zoom_to = zoom_to

    def getBoundaries(self):
        if self.boundaries:
            return self.boundaries
        boundaries = self.geojson.getBoundaries()
        return boundaries

    def getFill(self,geojson_props):
        if isinstance(self.value,str):
            if self.value in geojson_props:
                val = geojson_props[self.value]
            else:
                return self.default_fill_colour
        else:
            val = self.value(geojson_props)
        return self.palette.getColour(val)

    def getLabel(self,geojson_props):
        if self.labelPropertyName in geojson_props:
            return geojson_props[self.labelPropertyName]
        return ""

    def getPolygonStyle(self,geojson_props):
        return {
            "fill": self.getFill(geojson_props),
            "tooltip": self.getLabel(geojson_props),
            "label": self.getLabel(geojson_props),
            "stroke": self.stroke,
            "stroke_width": self.stroke_width
        }

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def build(self):
        self.geojson.configureLayer(self.ownermap,self.width,self.height,self.boundaries,self.projection,self.zoom_to)
        self.geojson.build()

    def draw(self,doc,cx,cy):
        self.geojson.draw(doc,cx,cy)
        with open(os.path.join(os.path.split(__file__)[0],"chloropleth.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc,self,jscode,"chloropleth",cx,cy,config)
        doc.getDiagram().connect(self,"zoom",self.geojson,"zoom")
        doc.getDiagram().connect(self,"visible_window",self.geojson,"visible_window")