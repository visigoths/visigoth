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
import os
import os.path

from math import radians,sin,cos,pi,sqrt,log

from visigoth.svg import polygon, circle, line, rectangle, clip_path
from visigoth.map_layers import MapLayer
from visigoth.map_layers.geoplot import Geoplot, Multipoint
from visigoth.utils.js import Js
from visigoth.containers.box import Box
from visigoth.utils.mapping import Mapping

class Scatter(MapLayer):

    """
    Create a Scatter plot

    Arguments:
        data(list) : list of (lon,lat) pairs to plot

    Keyword Arguments:
        fill (str or function): fill colour for circles
        stroke (str): stroke colour for circles representing points
        stroke_width (int): stroke width for circles representing points
        radius (int): radius of circles representing points
        marker (bool): plot a marker rather than circle
    """

    def __init__(self, data, fill="grey",stroke="black",stroke_width=1,radius=5,marker=False):
        super(Scatter, self).__init__()
        self.data = data
        self.width = None
        self.height = None
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.radius = radius
        self.points = []
        self.boundaries = None
        self.scale  = None
        self.projection = None
        self.geoplot = None
        self.ownermap = None
        self.marker = marker

    def getBoundaries(self):
        if not self.boundaries:
            self.boundaries = Mapping.getBoundingBox(self.data,0.05)
        return self.boundaries

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
        self.ownermap = ownermap
        self.width = width
        self.height = height
        self.boundaries = boundaries
        self.projection = projection
        self.zoom_to = zoom_to

    def getWidth(self):
        return self.geoplot.getWidth()

    def getHeight(self):
        return self.geoplot.getHeight()

    def build(self):
        multipoints = []
        for point in self.data:
            multipoints.append(Multipoint([point],marker=self.marker,radius=self.radius,fill=self.fill,stroke=self.stroke,stroke_width=self.stroke_width))

        self.geoplot = Geoplot(multipoints=multipoints)
        self.geoplot.configureLayer(self.ownermap,self.width,self.height,self.boundaries,self.projection,self.zoom_to)
        self.geoplot.build()
        

    def draw(self,doc,cx,cy):
        self.geoplot.draw(doc,cx,cy)
        with open(os.path.join(os.path.split(__file__)[0],"scatter.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = { "geoplot_id":self.geoplot.getId() }
        Js.registerJs(doc,self,jscode,"scatter",cx,cy,config)
        doc.getDiagram().connect(self,"zoom",self.geoplot,"zoom")
        doc.getDiagram().connect(self,"visible_window",self.geoplot,"visible_window")
        

        
    