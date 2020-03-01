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

import random
import sys

from math import radians,sin,cos,pi,sqrt,log

from visigoth.svg import circle, line, text, path
from visigoth.utils.elements.axis import Axis
from visigoth.utils.data import Dataset

class Line(ChartElement):

    """
    Create an Line plot

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)
        
    Keyword Arguments:
        x (str or int): Identify the column to specify x-axis point value
        y (str or int): Identify the column to specify y-axis point value
        line (str or int): Identify the column to specify the line to which each point belongs 
        id (str or int): Identify the column to define the unique id of each point
        colour (str or int): Identify the column to define the line colour 
        label (str or int): Identify the column to define the label of each point
        width(int) : the width of the plot including axes
        height(int) : the height of the plot including axes
    
        lines(list) : line data in the form [(category,label,[(x,y)])]
    
        draw_grid (boolean): whether to draw gridlines
        smoothing (float) : smoothing factor to apply to lines, 0.0=no smoothing
        line_width (int) : width of the lines
        point_radius (int) : radius of points
        x_axis_label(str) : label for the x axis
        y_axis_label(str) : label for the y axis
        stroke (str): stroke color for circumference of points
        stroke_width (int): stroke width for circumference of points
        font_height (int): the height of the font for text labels
        text_attributes (dict): SVG attribute name value pairs to apply to labels
        x_axis_max (int|float): set the maximum value on the x axis
        x_axis_min (int|float): set the minimum value on the x axis
        y_axis_max (int|float): set the maximum value on the y axis
        y_axis_min (int|float): set the minimum value on the y axis
    """

    def __init__(self, data,x=0,y=1,line=None,id=None,colour=None,label=None,width=768, height=768, palette=None, draw_grid=True, smoothing=0.3, line_width=4, point_radius=4, x_axis_label=None, y_axis_label=None, stroke="black",stroke_width=2,font_height=24, text_attributes={},x_axis_max=None, x_axis_min=None, y_axis_max=None, y_axis_min=None):
        super(Line, self).__init__()
        self.setTooltipFunction(lambda cat,val: "%s: (%s,%s)"%(cat,str(val[0]),str(val[1])))
        self.dataset = Dataset(data)
        
        self.x = x
        self.y = y
        self.line = line
        self.id = id
        self.label = label
        self.colour = colour

        self.width = width
        self.height = height
        self.palette = palette
        
        if self.colour != None and not self.palette:
            if self.dataset.isDiscrete(self.colour):
                self.palette = DiscretePalette()
            else:
                self.palette = ContinuousPalette()
        
        self.draw_grid = draw_grid
        self.smoothing = smoothing
        self.line_width = line_width
        self.point_radius = point_radius

        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.stroke = stroke
        self.stroke_width = stroke_width

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

        if y_axis_min > 0 and not fix_y_max:
            y_axis_min = 0.0
        if y_axis_max < 0.0 and not fix_y_max:
            y_axis_max = 0.0

        self.configureXRange(x_axis_min,x_axis_max)
        self.configureYRange(y_axis_min,y_axis_max)
        ax = Axis(self.width,"horizontal",x_axis_min,x_axis_max,label=self.x_axis_label,font_height=self.font_height,text_attributes=self.text_attributes)
        ay = Axis(self.height,"vertical",y_axis_min,y_axis_max,label=self.y_axis_label,font_height=self.font_height,text_attributes=self.text_attributes)
        ax.build()
        ay.build()
        self.ax = Axis(self.width-ay.getWidth(),"horizontal",x_axis_min,x_axis_max,label=self.x_axis_label,font_height=self.font_height,text_attributes=self.text_attributes)
        self.ay = Axis(self.height-ax.getHeight(),"vertical",y_axis_min,y_axis_max,label=self.y_axis_label,font_height=self.font_height,text_attributes=self.text_attributes)

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

    def drawLines(self,diagram,cx,cy,ox,oy,categories):

        def plotpoint(diagram,x,y,cat):
            col = self.palette.getColour(cat)

            cx = self.computeX(x)
            cy = self.computeY(y)
            circ = circle(cx,cy,self.point_radius,col,tooltip=self.getTooltip(cat,(x,y)))

            circ.addAttr("stroke",self.stroke)
            circ.addAttr("stroke-width",self.stroke_width)
            ids = categories.get(cat,[])
            ids.append(circ.getId())
            categories[cat] = ids
            diagram.add(circ)

        def plotline(linepoints):
            if not linepoints:
                return
            linepoints = sorted(linepoints,key=lambda p:p[0])
            linecat = linepoints[0][2]
            coords = [(self.computeX(x),self.computeY(y)) for (x,y,_) in linepoints]
            p = path(coords,self.palette.getColour(linecat),self.stroke_width,smoothing=self.smoothing)
            
            ids = categories.get(linecat,[])
            ids.append(p.getId())
            categories[linecat] = ids

            diagram.add(p)

            for (x,y,col) in linepoints:
                plotpoint(diagram,x,y,col)

        if self.line != None:
            lines = map(lambda x:x[0],self.dataset.query([self.line],unique=True))
            for line in lines:
                linepoints = self.dataset.query([self.x,self.y,self.colour],filters=[self.dataset.filter(self.line,"=",line)])
                plotline(linepoints)
        else:
            linepoints = self.dataset.query([self.x,self.y,self.colour])
            plotline(linepoints)

    def drawChart(self,doc,cx,cy):
        ox = cx - self.getWidth()/2
        oy = cy - self.getHeight()/2

        self.configureChartArea(ox+self.ay.getWidth(),oy,self.chart_width,self.chart_height)

        categories = {}

        self.drawLines(doc,cx,cy,ox,oy,categories)

        if self.draw_grid:
            self.drawGrid(doc)

        self.ax.draw(doc,ox+self.ay.getWidth()+self.chart_width/2,oy+self.chart_height+self.ax.getHeight()/2)
        self.ay.draw(doc,ox+self.ay.getWidth()/2,oy+self.chart_height/2)

        return {"categories":categories}