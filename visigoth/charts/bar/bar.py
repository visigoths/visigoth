# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#   and associated documentation files (the "Software"), to deal in the Software without
#   restriction, including without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or
#   substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from visigoth.charts import ChartElement
from visigoth.svg import rectangle,text,line
from visigoth.common.axis import Axis
from visigoth.utils.data import Dataset
from visigoth.utils.colour import DiscretePalette, ContinuousPalette

class Bar(ChartElement):
    """
    Create a Bar Chart

    Arguments:
        data (dict): A relational data set (for example, list of dicts/lists/tuples describing each row)
    
    Keyword Arguments:    
        x (str or int): Identify the column to yield discrete values
        y (str or int): Identify the column to measure on the y-axis (use count if not specified)
        colour (str or int): Identify the column to define the bar colour (use palette default colour if not specified)
        stacked (bool): When colour is defined, choose wether to stack coloured bars or display them side by side
        width (int): the width of the plot in pixels
        height (int): the height of the plot in pixels
        palette(list) : a DiscretePalette|ContinuousPalette object
        stroke (str): stroke color for bars
        stroke_width (int): stroke width for bars
        font_height (int): the height of the font for text labels
        spacing_fraction (float) : ratio of bar width to spacing
        text_attributes (dict): SVG attribute name value pairs to apply to labels
        labelfn (lambda): function to compute a label string, given a category and numeric value
    """
    def __init__(self,data,x=0,y=1,colour=None,stacked=True,width=512,height=512,palette=None,stroke="black",stroke_width=2,font_height=12,spacing_fraction=0.1,text_attributes={},labelfn=None):
        super(Bar, self).__init__()
        self.dataset = Dataset(data)
        self.setDrawGrid(True)
        self.x = x
        self.y = y
        self.colour = colour
        self.width = width
        self.height = height
        self.stacked = stacked
        self.font_height = font_height
        self.spacing_fraction = spacing_fraction
        self.text_attributes = text_attributes
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.labelfn = labelfn
        
        if not palette:
            if self.colour is None or self.dataset.isDiscrete(self.colour):
                palette = DiscretePalette()
            else:
                palette = ContinuousPalette()
        self.setPalette(palette)

        querycols = [self.x]
        if self.y != None:
            querycols.append(self.y)
        else:
            querycols.append(Dataset.constant(1))

        if self.colour != None:
            querycols.append(self.colour)

        self.data = self.dataset.query(querycols)
        self.colourvals = []
        if self.colour is not None:
            for v in self.dataset.query([self.colour],unique=True,flatten=True):
                self.getPalette().allocateColour(v)
                self.colourvals.append(v)
        self.colourvals = sorted(self.colourvals)

        self.setMargins(10,self.font_height*1.5)

        agg_fns = []
        if self.y:
            if self.stacked:
                agg_fns.append(Dataset.sum(self.y))
            else:
                agg_fns.append(Dataset.max(self.y))
        else:
            agg_fns.append(Dataset.count())

        bar_totals = self.dataset.query([self.x],unique=True,aggregations=agg_fns)
        
        self.bar_keys = list(map(lambda x:x[0],bar_totals))
        self.bar_values = list(map(lambda x:x[1],bar_totals))

        self.valuemax=max(self.bar_values)
        self.valuemin=min(self.bar_values)
        if self.valuemin >= 0:
            self.valuemin = 0

        self.configureYRange(self.valuemin,self.valuemax)

        y_axis = Axis(self.height,"vertical",self.valuemin,self.valuemax)
        x_axis = Axis(self.height, "horizontal", discreteValues=self.bar_keys)
        if isinstance(self.x,str):
            x_axis.setLabel(self.x)
        if isinstance(self.y,str):
            y_axis.setLabel(self.y)
        self.setAxes(x_axis,y_axis)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def drawChart(self,doc,cx,cy,width,height):

        categories = {}
        
        barcount = len(self.data)
        barwidth = width / barcount

        def compute_segments(key):
            if not self.y:
                return self.dataset.query([self.colour],aggregations=[Dataset.count()],filters=[Dataset.filter(self.x,"=",key)])
            else:
                return self.dataset.query([self.colour],aggregations=[Dataset.sum(self.y)],filters=[Dataset.filter(self.x,"=",key)])
                
        for index in range(len(self.bar_keys)):

            barkey = self.bar_keys[index]
            barvalue = self.bar_values[index]

            bx = self.computeX(barkey)

            if self.colour and self.colour != self.x:
                segments = compute_segments(barkey)
            else:
                segments = [(barkey,barvalue)]

            s = sum([v for (k,v) in segments])
            total = s
            lastvalue = 0

            if self.stacked or not self.colour:
                # stacked bars
                for (cat,value) in segments:
                    if self.colour is not None:
                        colour = self.palette.getColour(cat)
                    else:
                        colour = self.palette.getDefaultColour()
                    y1 = self.computeY(value)
                    y0 = self.computeY(lastvalue)

                    bh = abs(y1-y0)
                    bt = min(y0,y1)

                    r = rectangle(bx-(1-self.spacing_fraction)*barwidth*0.5,bt,barwidth*(1-self.spacing_fraction),bh,colour,stroke=self.stroke,stroke_width=self.stroke_width,tooltip=self.getTooltip(cat,value))

                    categories[cat] = [r.getId()]
                    doc.add(r)
                    lastvalue = value
            else:
                # display thin bars, side by side
                segment_vals = {}
                bw = (1 - self.spacing_fraction) * barwidth / len(self.colourvals)
                x = bx-(1-self.spacing_fraction)*barwidth*0.5
                for (cat, value) in segments:
                    segment_vals[cat] = value
                for cat in self.colourvals:
                    value = segment_vals.get(cat,0)
                    colour = self.palette.getColour(cat)
                    y0 = self.computeY(0)
                    y1 = self.computeY(value)
                    bh = abs(y1 - y0)
                    bt = min(y0, y1)

                    r = rectangle(x, bt, bw, bh, colour, stroke=self.stroke,
                            stroke_width=self.stroke_width, tooltip=self.getTooltip(cat, value))
                    x += bw
                    categories[cat] = [r.getId()]
                    doc.add(r)

            if self.labelfn:
                # display the label above the bar
                value_str = self.labelfn(barkey,total)
                ty = bt-self.font_height*0.2
                t = text(bx,ty,value_str)
                t.addAttr("font-size",self.font_height)
                t.addAttrs(self.text_attributes)
                doc.add(t)

        _, yAxis = self.getAxes()
        if yAxis.getMinValue() < 0 and yAxis.getMaxValue() > 0:
            # draw horizontal axis line at 0
            axis = line(cx-width/2,self.computeY(0),cx+width/2,self.computeY(0),self.stroke,self.stroke_width)
            doc.add(axis)
        return {"categories":categories}