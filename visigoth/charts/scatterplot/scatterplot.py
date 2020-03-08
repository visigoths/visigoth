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

from visigoth.charts import ChartElement
from visigoth.containers.box import Box
from visigoth.utils.data import Dataset
from visigoth.utils.colour import DiscretePalette, ContinuousPalette

import random
import sys

from math import radians,sin,cos,pi,sqrt,log

from visigoth.svg import circle, line, text
from visigoth.utils.elements.axis import Axis
from visigoth.utils.marker import MarkerManager

class ScatterPlot(ChartElement):

    """
    Create a Scatter plot

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)
    
    Keyword Arguments:
        x (str or int): Identify the column to provide the x-axis value for each point
        y (str or int): Identify the column to provide the y-axis value for each point
        width(int) : the width of the plot including axes
        height(int) : the height of the plot including axes
        colour (str or int): Identify the column to define the point colour (use fill colour if not specified)
        label (str or int): Identify the column to define the label
        radius (str or int): Identify the column to define the radius
        fixed_radius (float): radius to use for all points if radius not specified
        palette(object) : a ContinuousPalette or DiscretePalette object
        marker_manager(object) : a MarkerManager object
        stroke (str): stroke color for circumference of points
        stroke_width (int): stroke width for circumference of points
        fill (str): colour for points if not defined by colour keyword argument
        font_height (int): the height of the font for text labels
        text_attributes (dict): SVG attribute name value pairs to apply to labels
    """

    def __init__(self, data, x=0, y=1, width=768, height=768, colour=None, label=None, radius=None, fixed_radius=3, palette=None, marker_manager=None, stroke="black",stroke_width=2,fill="grey",font_height=24, text_attributes={}):
        super(ScatterPlot, self).__init__()
        self.setTooltipFunction(lambda cat,val: "%s %s: (%.02f,%.02f)"%(cat[0],cat[1],val[0],val[1]))
        self.dataset = Dataset(data)
        self.setDrawGrid(True)
        self.x = x
        self.y = y
        self.colour = colour
        self.radius = radius
        self.fixed_radius = fixed_radius
        self.label = label

        self.width = width
        self.height = height
        
        if self.colour != None and not palette:
            if self.dataset.isDiscrete(self.colour):
                palette = DiscretePalette()
            else:
                palette = ContinuousPalette()
        self.setPalette(palette)

        if not marker_manager:
            marker_manager = MarkerManager()
        self.setMarkerManager(marker_manager)

        self.font_height = font_height
        self.text_attributes = text_attributes
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.fill = fill

        xy_range = self.dataset.query(aggregations=[Dataset.min(self.x),Dataset.max(self.x),Dataset.min(self.y),Dataset.max(self.y)])[0]
        
        (x_axis_min,x_axis_max,y_axis_min,y_axis_max) = tuple(xy_range)

        x_label = "X"
        y_label = "Y"
        if isinstance(self.x,str):
            x_label = self.x
        if isinstance(self.y,str):
            y_label = self.y

        ax = Axis(self.width,"horizontal",x_axis_min,x_axis_max,label=x_label,font_height=self.font_height,text_attributes=self.text_attributes)
        ay = Axis(self.height,"vertical",y_axis_min,y_axis_max,label=y_label,font_height=self.font_height,text_attributes=self.text_attributes)
        
        self.setAxes(ax,ay)
        if self.colour:
            for v in self.dataset.query([self.colour],unique=True,flatten=True):
                self.getPalette().getColour(v)
        if self.radius:
            for v in self.dataset.query([self.radius],unique=True,flatten=True):
                self.getMarkerManager().noteSize(v)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def drawChart(self,doc,chart_cx,chart_cy,chart_width,chart_height):        
        
        categories = {}
        def plot(doc,x,y,v,label,r):
            if v != None:
                col = self.palette.getColour(v)
            else:
                col = self.fill

            cx = self.computeX(x)
            cy = self.computeY(y)

            marker = self.getMarkerManager().getMarker(r,self.fixed_radius)
            return marker.plot(doc,cx,cy,self.getTooltip((label,v),(x,y)),col,self.stroke,self.stroke_width)

        for (x,y,label,v,r) in self.dataset.query([self.x,self.y,self.label,self.colour,self.radius]):
            cid = plot(doc,x,y,v,label,r)
            if v:
                ids = categories.get(v,[])
                ids.append(cid)
                categories[v] = ids

        return {"categories":categories}