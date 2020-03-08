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

import os.path

from visigoth.common import DiagramElement
from visigoth.svg import line
from visigoth.utils.js import Js

class ChartElement(DiagramElement):

    def __init__(self):
        super(ChartElement,self).__init__()
        self.setTooltipFunction()
        self.setGridStyle()
        self.palette = None
        self.marker_manager = None
        self.xAxis = None
        self.yAxis = None
        self.draw_grid = False

    def setDrawGrid(self,draw_grid):
        self.draw_grid = draw_grid

    def setPalette(self,palette):
        self.palette = palette

    def getPalette(self):
        return self.palette

    def setMarkerManager(self,marker_manager):
        self.marker_manager = marker_manager

    def getMarkerManager(self):
        return self.marker_manager

    def setAxes(self,xAxis,yAxis):
        self.xAxis = xAxis
        self.yAxis = yAxis

    def getAxes(self):
        return (self.xAxis,self.yAxis)

    def setGridStyle(self,stroke="grey",stroke_width=1):
        self.grid_stroke = stroke
        self.grid_stroke_width = stroke_width

    def setTooltipFunction(self,fn = lambda cat,val: "%s: %0.2f"%(cat,val)):
        self.tooltip_fn = fn

    def getTooltip(self,cat,val):
        return self.tooltip_fn(cat,val)

    def configureXRange(self,axis_min,axis_max):
        self.x_axis_min = axis_min
        self.x_axis_max = axis_max

    def configureYRange(self,axis_min,axis_max):
        self.y_axis_min = axis_min
        self.y_axis_max = axis_max

    def getXRange(self):
        return (self.x_axis_min,self.x_axis_max)

    def getYRange(self):
        return (self.y_axis_min,self.y_axis_max)

    def configureChartArea(self,ox,oy,width,height):
        self.chart_ox = ox
        self.chart_oy = oy
        self.chart_width = width
        self.chart_height = height

    def computeX(self,value):
        return self.xAxis.getPointPosition(self.chart_ox,value)

    def computeY(self,value):
        return self.yAxis.getPointPosition(self.chart_oy,value)

    def build(self):
        x_axis_height = 0
        y_axis_width = 0

        if self.xAxis:
            self.xAxis.build()
            x_axis_height = self.xAxis.getHeight()
        if self.yAxis:
            self.yAxis.build()
            y_axis_width = self.yAxis.getWidth()
        
        if self.xAxis:
            self.xAxis.setLength(self.getWidth()-y_axis_width)
        if self.yAxis:
            self.yAxis.setLength(self.getHeight()-x_axis_height)
        
        if self.xAxis:
            self.xAxis.build()
            x_axis_height = self.xAxis.getHeight()
        if self.yAxis:
            self.yAxis.build()
            y_axis_width = self.yAxis.getWidth()
        
        self.chart_width = self.getWidth() - y_axis_width
        self.chart_height = self.getHeight() - x_axis_height

    def drawGrid(self,doc):

        if self.yAxis:
            y_ticks = self.yAxis.getTickPositions(self.chart_oy)
            x1 = self.chart_ox
            x2 = self.chart_ox + self.chart_width
            for y in y_ticks:
                l = line(x1,y,x2,y,self.grid_stroke,self.grid_stroke_width)
                doc.add(l)

        if self.xAxis:
            x_ticks = self.xAxis.getTickPositions(self.chart_ox)
            y1 = self.chart_oy
            y2 = self.chart_oy + self.chart_height
            for x in x_ticks:
                l = line(x,y1,x,y2,self.grid_stroke,self.grid_stroke_width)
                doc.add(l)

    def draw(self,doc,cx,cy):
        # self.openClip(doc,cx,cy)
        ox = cx - self.getWidth()/2
        oy = cy - self.getHeight()/2

        chart_height = self.getHeight()
        chart_width = self.getWidth()

        x_axis_height = 0
        if self.xAxis:
            x_axis_min = self.xAxis.getMinValue()
            x_axis_max = self.xAxis.getMaxValue()
            self.configureXRange(x_axis_min,x_axis_max)
            x_axis_height = self.xAxis.getHeight()
            chart_height -= x_axis_height

        y_axis_width = 0
        if self.yAxis:
            y_axis_min = self.yAxis.getMinValue()
            y_axis_max = self.yAxis.getMaxValue()
            self.configureYRange(y_axis_min,y_axis_max)
            y_axis_width = self.yAxis.getWidth()
            chart_width -= y_axis_width

        self.configureChartArea(ox+y_axis_width,oy,chart_width,chart_height)

        if self.xAxis:
            self.xAxis.draw(doc,ox+y_axis_width+self.chart_width/2,oy+self.chart_height+x_axis_height/2)
        if self.yAxis:
            self.yAxis.draw(doc,ox+y_axis_width/2,oy+self.chart_height/2)

        if self.draw_grid:
            self.drawGrid(doc)
    
        chart_cx = ox + y_axis_width + chart_width/2
        chart_cy = oy + chart_height/2
        config = self.drawChart(doc,chart_cx,chart_cy,chart_width,chart_height)

        # self.closeClip(doc)

        with open(os.path.join(os.path.split(__file__)[0],"chart_element.js"),"r") as jsfile:
            jscode = jsfile.read()
        Js.registerJs(doc,self,jscode,"chart_element",cx,cy,config)