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
from visigoth.utils.marker import MarkerManager
from visigoth.utils.colour import DiscretePalette, ContinuousPalette

class Line(ChartElement):

    """
    Create an Line plot

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)
        
    Keyword Arguments:
        x (str or int): Identify the column to specify x-axis point value
        y (str or int): Identify the column to specify y-axis point value
        colour (str or int): Identify the column to specify the line to which each point belongs 
        id (str or int): Identify the column to define the unique id of each point
        label (str or int): Identify the column to define the label of each point
        size (str or int): Identify the column to determine the size of each point
        width(int) : the width of the plot including axes
        height(int) : the height of the plot including axes
        palette(object) : a ContinuousPalette or DiscretePalette instance to control line colour
        marker_manager(object) : a MarkerManager instance to control marker appearance
        smoothing (float) : smoothing factor to apply to lines, 0.0=no smoothing
        line_width (int) : specify the width of the lines in pixels
        font_height (int): the height of the font for text labels
        text_attributes (dict): SVG attribute name value pairs to apply to labels
    """

    def __init__(self, data,x=0,y=1,id=None,colour=None,label=None,size=None,width=768, height=768, palette=None, marker_manager=None, smoothing=0.0, line_width=2, font_height=24, text_attributes={}):
        super(Line, self).__init__()
        self.setTooltipFunction(lambda cat,val: "%s: (%s,%s)"%(cat,str(val[0]),str(val[1])))
        self.dataset = Dataset(data)
        self.setDrawGrid(True)
        self.x = x
        self.y = y
        self.id = id
        self.label = label
        self.colour = colour
        self.size = size
        self.width = width
        self.height = height
        
        if not palette:
            if self.colour == None or self.dataset.isDiscrete(self.colour):
                palette = DiscretePalette()
            else:
                palette = ContinuousPalette()
        self.setPalette(palette)

        if not marker_manager:
            marker_manager = MarkerManager()
        self.setMarkerManager(marker_manager)
        
        self.smoothing = smoothing
        self.line_width = line_width
        
        self.font_height = font_height
        self.text_attributes = text_attributes
        
        xy_range = self.dataset.query(aggregations=[Dataset.min(self.x),Dataset.max(self.x),Dataset.min(self.y),Dataset.max(self.y)])[0]
        
        (x_axis_min,x_axis_max,y_axis_min,y_axis_max) = tuple(xy_range)

        x_label = "X"
        y_label = "Y"
        if isinstance(self.x,str):
            x_label = self.x
        if isinstance(self.y,str):
            y_label = self.y

        if self.colour != None:
            for val in self.dataset.query([self.colour],unique=True,flatten=True):
                self.getPalette().getColour(val)

        if self.size:
            for v in self.dataset.query([self.size],unique=True,flatten=True):
                self.getMarkerManager().noteSize(v)

        ax = Axis(self.width,"horizontal",x_axis_min,x_axis_max,label=x_label,font_height=self.font_height,text_attributes=self.text_attributes)
        ay = Axis(self.height,"vertical",y_axis_min,y_axis_max,label=y_label,font_height=self.font_height,text_attributes=self.text_attributes)
        self.setAxes(ax,ay)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

        
    def drawChart(self,doc,chart_cx,chart_cy,chart_width,chart_height):
        
        categories = {}

        def plotpoint(x,y,cat,col,sz):
            cx = self.computeX(x)
            cy = self.computeY(y)

            marker = self.getMarkerManager().getMarker(sz)
            cid = marker.plot(doc,cx,cy,self.getTooltip(cat,(x,y)),col)

            ids = categories.get(cat,[])
            ids.append(cid)
            categories[cat] = ids
            
        def plotline(linepoints,linecat):
            if not linepoints:
                return
            linepoints = sorted(linepoints,key=lambda p:p[0])
            coords = [(self.computeX(x),self.computeY(y)) for (x,y,_) in linepoints]

            if self.palette:
                col = self.palette.getColour(linecat)
            else:
                col = self.palette.getDefaultColour()

            p = path(coords,col,self.line_width,smoothing=self.smoothing)
            
            ids = categories.get(linecat,[])
            ids.append(p.getId())
            categories[linecat] = ids

            doc.add(p)

            for (x,y,sz) in linepoints:
                plotpoint(x,y,linecat,col,sz)

        if self.colour != None:
            linecats = map(lambda x:x[0],self.dataset.query([self.colour],unique=True))
            for linecat in linecats:
                linepoints = self.dataset.query([self.x,self.y,self.size],filters=[self.dataset.filter(self.colour,"=",linecat)])
                plotline(linepoints,linecat)
        else:
            linepoints = self.dataset.query([self.x,self.y,self.size])
            plotline(linepoints,"")

        return {"categories":categories}