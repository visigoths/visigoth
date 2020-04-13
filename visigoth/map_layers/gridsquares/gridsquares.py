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
import os
import os.path

from visigoth.utils.mapping import Metadata
from visigoth.svg import line, text
from visigoth.map_layers import MapLayer
from visigoth.common.axis import Axis
from visigoth.utils.js import Js

class GridSquares(MapLayer):
    """
    Draw grid squares with lon/lat labels

    Keyword Arguments:
        decimal_places(int): the number of decimal places to display in labels
        stroke(str): stroke colour for grid line
        stroke_width(int): width of grid line
        font_height(int): the grid label font size in pixels 
        text_attributes(dict): a dict containing SVG name/value pairs
    """
    def __init__(self,decimal_places=3,stroke="black",stroke_width=1,font_height=12,text_attributes={ "fill":"white" }):
        super(GridSquares, self).__init__(Metadata(name="Grid"))
        self.bounds = None
        self.width = None
        self.projection = None
        self.x_axis = None
        self.y_axis = None
        self.axis_format = "%."+str(decimal_places)+"f"
        self.labelfn = lambda v: self.axis_format%(v)
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.font_height = font_height
        self.text_attributes = text_attributes

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
        self.ownermap = ownermap
        self.width = width
        self.height = height
        self.bounds = boundaries
        self.projection = projection
        self.zoom_to = zoom_to
            
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def build(self):
        ((lonmin,latmin),(lonmax,latmax)) = self.bounds
        self.x_axis = Axis(self.width,"horizontal",lonmin,lonmax,projection=self.projection)
        self.x_axis.build()
        self.y_axis = Axis(self.height,"vertical",latmin,latmax,projection=self.projection)
        self.y_axis.build()

    def getBoundaries(self):
        return self.bounds

    def draw(self,doc,cx,cy):
        ox = cx - self.width/2
        oy = cy - self.height/2

        y_ticks = self.y_axis.getTickPositions(oy)
        tps = self.y_axis.getTickPoints()

        lines = []
        labels = []

        x1 = ox
        x2 = ox + self.width
        idx = 0
        for y in y_ticks:
            l = line(x1,y,x2,y,self.stroke,self.stroke_width)
            doc.add(l)
            t = text(x1,y,self.labelfn(tps[idx]),font_height=self.font_height,text_attributes=self.text_attributes)
            t.setHorizontalCenter(False)
            doc.add(t)
            lines.append(l.getId())
            labels.append(t.getId())
            idx += 1

        x_ticks = self.x_axis.getTickPositions(ox)
        tps = self.x_axis.getTickPoints()
        y1 = oy
        y2 = oy + self.height
        idx = 0
        for x in x_ticks:
            l = line(x,y1,x,y2,self.stroke,self.stroke_width)
            doc.add(l)
            lines.append(l.getId())
            t = text(x,y1,self.labelfn(tps[idx]),font_height=self.font_height,text_attributes=self.text_attributes)
            t.setRotation(math.pi/2)
            t.setHorizontalCenter(False)
            doc.add(t)
            idx += 1
            labels.append(t.getId())
        with open(os.path.join(os.path.split(__file__)[0],"gridsquares.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = { "lines": lines, "stroke_width": self.stroke_width, "labels": labels, "font_height":self.font_height }
        Js.registerJs(doc,self,jscode,"gridsquares",cx,cy,config)
        
        

        