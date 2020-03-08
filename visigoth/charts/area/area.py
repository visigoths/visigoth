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
from visigoth.utils.colour.palette import DiscretePalette
from visigoth.utils.data import Dataset

class Area(ChartElement):

    """
    Create a stacked area plot

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each point)
        
    Keyword Arguments:
        x (str or int): Identify the column to specify x-axis point value
        y (str or int): Identify the column to specify y-axis point value
        colour (str or int): Identify the column to define the area and colour 
        id (str or int): Identify the column to define the unique id of each point
        label (str or int): Identify the column to define the label of each point
        width(int) : the width of the plot including axes
        height(int) : the height of the plot including axes
        smoothing (float) : smoothing factor to apply to lines, 0.0=no smoothing
        line_width (int) : width of the lines
        point_radius (int) : radius of points
        stroke (str): stroke color for circumference of points
        stroke_width (int): stroke width for circumference of points
        fill (str): the default fill colour for areas
        font_height (int): the height of the font for text labels
        text_attributes (dict): SVG attribute name value pairs to apply to labels
    """

    def __init__(self, data, x=0, y=1, colour=2, id=None, label=None, width=768, height=768,  palette=None, smoothing=0.0, line_width=4, point_radius=4, stroke="black",stroke_width=2, fill="blue", font_height=24, text_attributes={}):
        super(Area, self).__init__()
        self.setTooltipFunction(lambda cat,val: "%s: (%s,%s)"%(cat,str(val[0]),str(val[1])))
        self.setDrawGrid(True)
        self.x = x
        self.y = y
        self.colour = colour
        self.id = id
        self.label = label

        self.data = Dataset(data)

        self.xcs = sorted(self.data.query([self.x],unique=True,flatten=True))
        if self.colour:
            self.cats = self.data.query([self.colour],unique=True,flatten=True)
        else:
            self.cats = []

        self.width = width
        self.height = height
    
        if self.colour and not palette:
            palette = DiscretePalette()
            for cat in self.cats:
                palette.getColour(cat)

        self.setPalette(palette)

        self.smoothing = smoothing
        self.line_width = line_width
        self.point_radius = point_radius

        self.font_height = font_height
        self.text_attributes = text_attributes
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.fill = fill

        self.catmap = {} # mapping from colour-category to list of SVG ids

        x_axis_max = max(x for x in self.xcs)
        x_axis_min = min(x for x in self.xcs)

        sumy_over_x = self.data.query([self.x],aggregations=[Dataset.sum(self.y)])
        y_axis_max = max([y for (x,y) in sumy_over_x]) 
        y_axis_min = min([y for (x,y) in sumy_over_x])

        # always start the y-axis at 0 to correctly represent areas
        y_axis_min = 0

        x_label = "X"
        y_label = "Y"
        if isinstance(self.x,str):
            x_label = self.x
        if isinstance(self.y,str):
            y_label = self.y
        
        ax = Axis(self.width,"horizontal",x_axis_min,x_axis_max,label=x_label,font_height=self.font_height,text_attributes=self.text_attributes)
        ay = Axis(self.height,"vertical",y_axis_min,y_axis_max,label=y_label,font_height=self.font_height,text_attributes=self.text_attributes)
        self.setAxes(ax,ay)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def plotPoint(self,diagram,cat,x,y,col):
        
        cx = self.computeX(x)
        cy = self.computeY(y)
        circ = circle(cx,cy,self.point_radius,col,tooltip=self.getTooltip(cat,(x,y)))

        circ.addAttr("stroke",self.stroke)
        circ.addAttr("stroke-width",self.stroke_width)
        if cat:
            ids = self.catmap.get(cat,[])
            ids.append(circ.getId())
            self.catmap[cat] = ids
        diagram.add(circ)

    def plotLine(self,diagram,cat,linepoints,col):
        coords = [(self.computeX(x),self.computeY(y)) for (x,y) in linepoints]
        
        p = path(coords,col,self.stroke_width,smoothing=self.smoothing)

        p.close([(self.computeX(self.getXRange()[1]),self.computeY(0)),(self.computeX(self.getXRange()[0]),self.computeY(0))])
        p.addAttr("fill",col)
        p.addAttr("stroke",self.stroke)
        if cat:
            ids = self.catmap.get(cat,[])
            ids.append(p.getId())
            self.catmap[cat] = ids

        diagram.add(p)

        for (x,y) in linepoints:
            self.plotPoint(diagram,cat,x,y,col)

    def drawArea(self,diagram):
        points = self.data.query([self.x,self.y,self.id,self.label])
        linepoints = [(x,y) for (x,y,_,_) in points]
        linepoints = sorted(linepoints,key=lambda p:p[0])
        self.plotLine(diagram,None,linepoints,self.fill)
            
    def drawAreas(self,diagram):
    
        catlines = {}
        catdata = {}

        for cat in self.cats:
            catdata[cat] = self.data.query([self.x,self.y,self.id,self.label],filters=[Dataset.filter(self.colour,"=",cat)])

        for x in self.xcs:
            yc = 0
            
            for cat in self.cats:
                points = catdata[cat]
                point = [(py,id,label) for (px,py,id,label) in points if px==x]
                if not point:
                    raise Exception("Invalid input data")
                else:
                    point = point[0]

                yc += point[0]
                    
                line = catlines.get(cat,[])
                line.append((x,yc))
                catlines[cat] = line

        revcats = self.cats
        revcats.reverse()
        for cat in revcats:
            linepoints = catlines[cat]
            linepoints = sorted(linepoints,key=lambda p:p[0])
            linecol = self.palette.getColour(cat)
            self.plotLine(diagram,cat,linepoints,linecol)
            
    def drawChart(self,doc,chart_cx,chart_cy,chart_width,chart_height):
        
        self.catmap = {}
        if self.cats:
            # draw stacked area chart
            self.drawAreas(doc)
        else:
            # draw single area chart
            self.drawArea(doc)

        if self.draw_grid:
            self.drawGrid(doc)

        return {"categories":self.catmap}