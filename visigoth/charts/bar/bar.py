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

class Bar(ChartElement):
    """
    Create a Bar Chart

    Arguments:
        data (dict): A list containing a (category,value)
        width (int): the width of the plot in pixels
        height (int): the height of the plot in pixels
        palette(list) : a DiscretePalette object

    Keyword Arguments:
        waterfall (boolean) : draw bars connected into a waterfall
        draw_axis (boolean) : draw a y-axis
        draw_grid (boolean) : draw grid lines
        stroke (str): stroke color for bars
        stroke_width (int): stroke width for bars
        font_height (int): the height of the font for text labels
        spacing_fraction (float) : ratio of bar width to spacing
        text_attributes (dict): SVG attribute name value pairs to apply to labels
        labelfn (lambda): function to compute a label string, given a category and numeric value
        axis_max (int|float): set the maximum value on the axis
        axis_min (int|float): set the minimum value on the axis
    """
    def __init__(self,data,width,height,palette,waterfall=False,draw_axis=True,draw_grid=True,stroke="black",stroke_width=2,font_height=24,spacing_fraction=0.1,text_attributes={},labelfn=lambda k,v:"%0.2f"%v, axis_max=None, axis_min=None):
        super(Bar, self).__init__()
        self.data = data
        self.width = width
        self.height = height
        self.palette = palette
        self.waterfall = waterfall
        self.draw_axis = draw_axis
        self.draw_grid = draw_grid
        self.font_height = font_height
        self.spacing_fraction = spacing_fraction
        self.text_attributes = text_attributes
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.labelfn = labelfn
        self.axis_max = axis_max
        self.axis_min = axis_min

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getYAxis(self):
        return self.axis

    def build(self):
        self.labelmarginx=10
        self.labelmarginy=self.font_height*1.5

        def total(v):
            if isinstance(v,list):
                return sum([v1 for (k1,v1) in v])
            else:
                return v

        values=[total(v) for (k,v) in self.data]
        if self.waterfall:
            waterfall_values = []
            acc = 0
            for value in values:
                acc += value
                waterfall_values.append(acc)
            values = waterfall_values
        if self.axis_max:
            self.valuemax = self.axis_max
        else:
            self.valuemax=max(values)
        if self.axis_min:
            self.valuemin = self.axis_min
        else:
            self.valuemin=min(values)
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
        for (outercat,outervalue) in self.data:

            if isinstance(outervalue,list):
                segments = outervalue
            else:
                segments = [(outercat,outervalue)]

            s = sum([v for (k,v) in segments])
            if self.waterfall:
                total += s
            else:
                total = s
            for (cat,value) in segments:
                colour = self.palette.getColour(cat)
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
                if self.waterfall:
                    value_str = self.labelfn(outercat,s)
                else:
                    value_str = self.labelfn(outercat,total)

                if value > 0:
                    ty = bt-self.font_height*0.2
                else:
                    ty = bb+self.font_height*1.2
                t = text(bx+barwidth/2,ty,value_str)
                tid = t.setId()
                t.addAttr("font-size",self.font_height)
                t.addAttrs(self.text_attributes)
                doc.add(t)

            if not self.waterfall:
                sy = oy
            else:
                # for waterfall charts,
                # add horizontal lines connecting successive bars
                if last_sy != None:
                    l = line(bx-barwidth+(self.spacing_fraction*0.5*barwidth),last_sy,bx+barwidth-(self.spacing_fraction*0.5*barwidth),last_sy,self.stroke,self.stroke_width)
                    doc.add(l)
                last_sy = sy
            bx += barwidth

        # horizontal axis
        axis = line(cx-width/2,oy,cx+width/2,oy,self.stroke,self.stroke_width)
        doc.add(axis)
        return {"categories":categories}