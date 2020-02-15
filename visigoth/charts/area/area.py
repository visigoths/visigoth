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

class Area(ChartElement):

    """
    Create a stacked area plot

    Arguments:
        data(list) : line data in the form [(x,[(category,label,height)])]
        width(int) : the width of the plotting area in pixels (not including x-axis)
        height(int) : the height of the plotting area in pixels (not including y-axis)
        palette(list) : a list of (category, colour) pairs

    Keyword Arguments:
        poscats(list): order of categories to draw above x-axis
        negcats(list): order of categories to draw below x-axis
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

    def __init__(self, data, width, height,  palette, poscats=[], negcats=[], draw_grid=True, smoothing=0.3, line_width=4, point_radius=4, x_axis_label=None, y_axis_label=None, stroke="black",stroke_width=2,font_height=24, text_attributes={},x_axis_max=None, x_axis_min=None, y_axis_max=None, y_axis_min=None):
        super(Area, self).__init__()
        self.setTooltipFunction(lambda cat,val: "%s: (%s,%s)"%(cat,str(val[0]),str(val[1])))
        self.data = data
        self.xcs = [ls[0] for ls in self.data]
        self.poscats = poscats
        self.negcats = negcats

        for cat in self.data[0][1].keys():
            if cat not in self.poscats and cat not in self.negcats:
                self.poscats.append(cat)

        self.width = width
        self.height = height
        self.palette = palette
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

        if x_axis_max == None:
            x_axis_max = max(x for x in self.xcs)
        if x_axis_min == None:
            x_axis_min = min(x for x in self.xcs)

        if y_axis_max == None:
            y_axis_max = 0
        if y_axis_min == None:
            y_axis_min = 0

        for (x,catdata) in self.data:
            ycs_pos = [catdata[cat][1] for cat in catdata.keys() if cat in self.poscats]
            ycs_neg = [-catdata[cat][1] for cat in catdata.keys() if cat in self.negcats]
            y_axis_max = max(y_axis_max,sum(ycs_pos))
            y_axis_min = min(y_axis_min,sum(ycs_neg))

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

    def drawAreas(self,diagram,cx,cy,ox,oy,categories):

        def plot(diagram,x,y,cat):
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

        catlines = {}
        for (x,catdata) in self.data:
            ypos = 0
            yneg = 0

            for cat in self.poscats+self.negcats:
                (_,h) = catdata[cat]
                if cat in self.poscats:
                    ypos += h
                    y = ypos
                elif cat in self.negcats:
                    yneg -= h
                    y = yneg
                else:
                    raise Exception("encountered unknown category: "+cat)
                line = catlines.get(cat,[])
                line.append((x,y))
                catlines[cat] = line

        drawcats = self.poscats+self.negcats
        drawcats.reverse()
        for linecat in drawcats:
            linepoints = catlines[linecat]
            linepoints = sorted(linepoints,key=lambda p:p[0])

            coords = [(self.computeX(x),self.computeY(y)) for (x,y) in linepoints]
            p = path(coords,self.palette.getColour(linecat),self.stroke_width,smoothing=self.smoothing)

            p.close([(self.computeX(self.getXRange()[1]),self.computeY(0)),(self.computeX(self.getXRange()[0]),self.computeY(0))])
            p.addAttr("fill",self.palette.getColour(linecat))
            p.addAttr("stroke",self.stroke)
            ids = categories.get(linecat,[])
            ids.append(p.getId())
            categories[linecat] = ids

            diagram.add(p)

            for (x,y) in linepoints:
                plot(diagram,x,y,linecat)

    def drawChart(self,doc,cx,cy):
        ox = cx - self.getWidth()/2
        oy = cy - self.getHeight()/2

        self.configureChartArea(ox+self.ay.getWidth(),oy,self.chart_width,self.chart_height)

        categories = {}

        self.drawAreas(doc,cx,cy,ox,oy,categories)

        if self.draw_grid:
            self.drawGrid(doc)

        self.ax.draw(doc,ox+self.ay.getWidth()+self.chart_width/2,oy+self.chart_height+self.ax.getHeight()/2)
        self.ay.draw(doc,ox+self.ay.getWidth()/2,oy+self.chart_height/2)

        return {"categories":categories}