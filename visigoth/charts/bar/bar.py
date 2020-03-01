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
import json

from visigoth.charts import ChartElement
from visigoth.svg import rectangle,text,line,javascript_snippet
from visigoth.utils.elements.axis import Axis
from visigoth.utils.data import Dataset
from visigoth.utils.colour import DiscretePalette

class Bar(ChartElement):
    """
    Create a Bar Chart

    Arguments:
        data (dict): A relational data set (for example, list of dicts/lists/tuples describing each row)
        x (str or int): Identify the column to yield discrete values

    Keyword Arguments:    
        y (str or int): Identify the column to measure on the y-axis (use count if not specified)
        colour (str or int): Identify the column to define the bar colour (use fill colour if not specified)
        width (int): the width of the plot in pixels
        height (int): the height of the plot in pixels
        palette(list) : a DiscretePalette object
        draw_axis (boolean) : draw a y-axis
        draw_grid (boolean) : draw grid lines
        stroke (str): stroke color for bars
        stroke_width (int): stroke width for bars
        fill (str): default colour for bars if colour is not specified
        font_height (int): the height of the font for text labels
        spacing_fraction (float) : ratio of bar width to spacing
        text_attributes (dict): SVG attribute name value pairs to apply to labels
        labelfn (lambda): function to compute a label string, given a category and numeric value
        axis_max (int|float): set the maximum value on the axis
        axis_min (int|float): set the minimum value on the axis
    """
    def __init__(self,data,x,y=None,colour=None,width=512,height=512,palette=None,draw_axis=True,draw_grid=True,stroke="black",stroke_width=2,fill="grey",font_height=24,spacing_fraction=0.1,text_attributes={},labelfn=lambda k,v:"%0.2f"%v, axis_max=None, axis_min=None):
        super(Bar, self).__init__()
        self.dataset = Dataset(data)
        self.x = x
        self.y = y
        self.colour = colour
        self.width = width
        self.height = height
        self.palette = palette
        self.draw_axis = draw_axis
        self.draw_grid = draw_grid
        self.font_height = font_height
        self.spacing_fraction = spacing_fraction
        self.text_attributes = text_attributes
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.fill = "grey"
        self.labelfn = labelfn
        self.axis_max = axis_max
        self.axis_min = axis_min

        if self.colour and not self.palette:
            self.palette = DiscretePalette()

        querycols = [self.x]
        if self.y != None:
            querycols.append(self.y)
        else:
            querycols.append(Dataset.constant(1))

        if self.colour != None:
            querycols.append(self.colour)

        self.data = self.dataset.query(querycols)
        if self.palette and self.colour != None:
            for tup in self.dataset.query([self.colour],unique=True):
                self.palette.getColour(tup[0])

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getYAxis(self):
        return self.axis

    def build(self):
        self.labelmarginx=10
        self.labelmarginy=self.font_height*1.5

        agg_fns = []
        if self.y:
            agg_fns.append(Dataset.sum(self.y))
        else:
            agg_fns.append(Dataset.count())
        bar_totals = self.dataset.query([self.x],unique=True,aggregations=agg_fns)
        
        self.bar_keys = list(map(lambda x:x[0],bar_totals))
        self.bar_values = list(map(lambda x:x[1],bar_totals))

        if self.axis_max:
            self.valuemax = self.axis_max
        else:
            self.valuemax=max(self.bar_values)
        if self.axis_min:
            self.valuemin = self.axis_min
        else:
            self.valuemin=min(self.bar_values)
            if self.valuemin >= 0:
                self.valuemin = 0

        self.configureYRange(self.valuemin,self.valuemax)

        self.axis = Axis(self.height-2*self.labelmarginy,"vertical",self.valuemin,self.valuemax)
        self.axis.build()

    def drawChart(self,doc,cx,cy):

        categories = {}
        if self.draw_axis:
            self.axis.draw(doc,cx-self.width/2+self.axis.getWidth()/2,cy)
            width = self.width - self.axis.getWidth()
            cx = cx - self.width/2 + self.axis.getWidth() + width/2
        else:
            width = self.width

        catcount = len(self.data)
        barwidth = (width - 4*self.labelmarginx) / catcount
        barheight = self.height - 2*self.labelmarginy

        self.configureChartArea(cx-width/2,cy-(self.height-2*self.labelmarginy)/2,width,barheight)
        if self.draw_grid:
            self.drawGrid(doc)

        bx = cx - width/2 + 2*self.labelmarginx

        valuerange = self.valuemax - self.valuemin

        oy = cy - self.height/2 + self.labelmarginy + barheight*(1-(-self.valuemin)/valuerange)
        sy = oy
        total = 0
        last_sy = None

        def compute_segments(key):
            if not self.y:
                return self.dataset.query([self.colour],aggregations=[Dataset.count()],filters=[Dataset.filter(self.x,"=",key)])
            else:
                return self.dataset.query([self.colour],aggregations=[Dataset.sum(self.y)],filters=[Dataset.filter(self.x,"=",key)])
                
        for index in range(len(self.bar_keys)):

            barkey = self.bar_keys[index]
            barvalue = self.bar_values[index]

            if self.colour and self.colour != self.x:
                segments = compute_segments(barkey)
            else:
                segments = [(barkey,barvalue)]

            s = sum([v for (k,v) in segments])
            total = s
            for (cat,value) in segments:
                if self.colour != None:
                    colour = self.palette.getColour(cat)
                else:
                    colour = self.fill
                bh = barheight*abs(value)/valuerange

                if value >= 0:
                    bb = sy
                    bt = sy - bh
                    sy = bt
                else:
                    bt = sy
                    bb = sy + bh
                    sy = bb
                r = rectangle(bx+(self.spacing_fraction*0.5*barwidth),bt,barwidth*(1-self.spacing_fraction),bb-bt,colour,stroke=self.stroke,stroke_width=self.stroke_width,tooltip=self.getTooltip(cat,value))

                categories[cat] = [r.getId()]
                doc.add(r)

            if self.labelfn:
                value_str = self.labelfn(barkey,total)

                if value > 0:
                    ty = bt-self.font_height*0.2
                else:
                    ty = bb+self.font_height*1.2
                t = text(bx+barwidth/2,ty,value_str)
                tid = t.setId()
                t.addAttr("font-size",self.font_height)
                t.addAttrs(self.text_attributes)
                doc.add(t)

            sy = oy
            bx += barwidth

        # horizontal axis
        axis = line(cx-width/2,oy,cx+width/2,oy,self.stroke,self.stroke_width)
        doc.add(axis)
        return {"categories":categories}