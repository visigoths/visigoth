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
        palette(list) : a ContinuousPalette or DiscretePalette object
        x_axis_label(str) : label for the x axis
        y_axis_label(str) : label for the y axis
        draw_grid(boolean) : whether to draw grid lines
        stroke (str): stroke color for circumference of points
        stroke_width (int): stroke width for circumference of points
        fill (str): colour for points if not defined by colour keyword argument
        font_height (int): the height of the font for text labels
        text_attributes (dict): SVG attribute name value pairs to apply to labels
        x_axis_max (int|float): set the maximum value on the x axis
        x_axis_min (int|float): set the minimum value on the x axis
        y_axis_max (int|float): set the maximum value on the y axis
        y_axis_min (int|float): set the minimum value on the y axis
    """

    def __init__(self, data, x=0, y=1, width=768, height=768, colour=None, label=None, radius=None, fixed_radius=3, palette=None, x_axis_label=None, y_axis_label=None, draw_grid=True, stroke="black",stroke_width=2,fill="grey",font_height=24, text_attributes={},x_axis_max=None, x_axis_min=None, y_axis_max=None, y_axis_min=None):
        super(ScatterPlot, self).__init__()
        self.setTooltipFunction(lambda cat,val: "%s %s: (%.02f,%.02f)"%(cat[0],cat[1],val[0],val[1]))
        self.dataset = Dataset(data)
        
        self.x = x
        self.y = y
        self.colour = colour
        self.radius = radius
        self.fixed_radius = fixed_radius
        self.label = label

        self.width = width
        self.height = height
        self.palette = palette

        if self.colour != None and not self.palette:
            if self.dataset.isDiscrete(self.colour):
                self.palette = DiscretePalette()
            else:
                self.palette = ContinuousPalette()
        
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.draw_grid = draw_grid
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.fill = fill

        xy_range = self.dataset.query(aggregations=[Dataset.min(self.x),Dataset.max(self.x),Dataset.min(self.y),Dataset.max(self.y)])[0]
        
        if x_axis_max == None:
            x_axis_max = xy_range[1]
        if x_axis_min == None:
            x_axis_min = xy_range[0]
        
        fix_y_max = (y_axis_max != None)
        fix_y_min = (y_axis_min != None)

        if y_axis_max == None:
            y_axis_max = xy_range[3]
        if y_axis_min == None:
            y_axis_min = xy_range[2]
        
        if y_axis_min > 0.0 and not fix_y_min:
            y_axis_min = 0.0
        if y_axis_max < 0.0 and not fix_y_max:
            y_axis_max = 0.0

        if x_axis_min == x_axis_max:
            x_axis_min -= 1.0
            x_axis_max += 1.0

        if y_axis_min == y_axis_max:
            y_axis_min -= 1.0
            y_axis_max += 1.0

        self.configureXRange(x_axis_min,x_axis_max)
        self.configureYRange(y_axis_min,y_axis_max)
        ax = Axis(self.width,"horizontal",x_axis_min,x_axis_max,label=self.x_axis_label,font_height=self.font_height,text_attributes=self.text_attributes)
        ay = Axis(self.height,"vertical",y_axis_min,y_axis_max,label=self.y_axis_label,font_height=self.font_height,text_attributes=self.text_attributes)
        ax.build()
        ay.build()
        self.ax = Axis(self.width-ay.getWidth(),"horizontal",x_axis_min,x_axis_max,label=self.x_axis_label,font_height=self.font_height,text_attributes=self.text_attributes)
        self.ay = Axis(self.height-ax.getHeight(),"vertical",y_axis_min,y_axis_max,label=self.y_axis_label,font_height=self.font_height,text_attributes=self.text_attributes)
        if self.colour:
            for v in self.dataset.query([self.colour],unique=True):
                self.palette.getColour(v[0])

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height


    def getXAxis(self):
        """
        Get the X-Axis

        Returns:
            :class:`visigoth.common.axis.Axis` object

        """
        return self.ax

    def getYAxis(self):
        """
        Get the Y-Axis

        Returns:
            :class:`visigoth.common.axis.Axis` object

        """
        return self.ay

    def build(self):
        self.ax.build()
        self.ay.build()
        self.chart_width = self.width - self.ay.getWidth()
        self.chart_height = self.height - self.ax.getHeight()
        self.palette.build()

    def drawChart(self,doc,cx,cy):
        ox = cx - self.getWidth()/2
        oy = cy - self.getHeight()/2

        self.configureChartArea(ox+self.ay.getWidth(),oy,self.chart_width,self.chart_height)

        if self.draw_grid:
            self.drawGrid(doc)

        self.ax.draw(doc,ox+self.ay.getWidth()+self.chart_width/2,oy+self.chart_height+self.ax.getHeight()/2)
        self.ay.draw(doc,ox+self.ay.getWidth()/2,oy+self.chart_height/2)

        categories = {}
        def plot(doc,x,y,v,label,r):
            if v != None:
                col = self.palette.getColour(v)
            else:
                col = self.fill

            if r == None:
                r = self.fixed_radius

            cx = self.computeX(x)
            cy = self.computeY(y)
            circ = circle(cx,cy,r,col,tooltip=self.getTooltip((label,v),(x,y)))

            circ.addAttr("stroke",self.stroke)
            circ.addAttr("stroke-width",self.stroke_width)
            doc.add(circ)
            return circ.getId()

        for (x,y,label,v,r) in self.dataset.query([self.x,self.y,self.label,self.colour,self.radius]):
            cid = plot(doc,x,y,v,label,r)
            ids = categories.get(v,[])
            ids.append(cid)
            categories[v] = ids

        return {"categories":categories}