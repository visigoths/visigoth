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
from visigoth.svg import rectangle, text, line
from visigoth.common.axis import Axis
from visigoth.utils.data import Dataset
from visigoth.utils.colour import DiscreteColourManager


class Histogram(ChartElement):
    """
    Create a Histogram Chart

    Arguments:
        data (dict): A relational data set (for example, list of dicts/lists/tuples describing each row)

    Keyword Arguments:
        x (str or int): Identify the column to yield continuous values
        colour (str or int): Identify the column to define the colour (use colour_manager default colour if not specified)
        nr_bin (int): The number of bins to create
        width (int): the width of the plot in pixels
        height (int): the height of the plot in pixels
        colour_manager(list) : a DiscreteColourManager object
        stroke (str): stroke color for bars
        stroke_width (int): stroke width for bars
        font_height (int): the height of the font for text labels
        spacing_fraction (float) : ratio of bar width to spacing
        text_attributes (dict): SVG attribute name value pairs to apply to labels
        labelfn (lambda): function to compute a label string, given a category and numeric value
    """

    def __init__(self, data, x=0, colour=None, nr_bins=15, width=512, height=512, colour_manager=None, stroke="black", stroke_width=2,
                 font_height=12, spacing_fraction=0.1, text_attributes={}, labelfn=lambda k, v: "%0.2f" % v):
        super().__init__()
        self.dataset = Dataset(data)
        self.setDrawGrid(True)
        self.x = x
        self.colour = colour
        self.nr_bins = nr_bins
        self.width = width
        self.height = height

        self.font_height = font_height
        self.spacing_fraction = spacing_fraction
        self.text_attributes = text_attributes
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.labelfn = labelfn

        if not colour_manager:
            colour_manager = DiscreteColourManager()
        self.setPalette(colour_manager)

        (x_min,x_max) = self.dataset.query(aggregations=[Dataset.min(self.x), Dataset.max(self.x)])[0]

        self.colourcats = []
        if self.colour != None:
            for cat in self.dataset.query([self.colour], unique=True, flatten=True):
                self.getPalette().allocateColour(cat)
                self.colourcats.append(cat)
        else:
            self.colourcats.append(None)

        self.data = {}
        for cat in self.colourcats:
            if cat == None:
                catdata = self.dataset.query([self.x],flatten=True)
            else:
                catdata = self.dataset.query([self.x],filters=[Dataset.filter(self.colour,"=",cat)],flatten=True)
            self.data[cat] = catdata

        self.setMargins(10, self.font_height * 1.5)

        self.intervals = []
        x_width = (x_max-x_min)/self.nr_bins
        for i in range(self.nr_bins):
            self.intervals.append((x_min+i*x_width,x_min+(i+1)*x_width))

        max_freq = 0
        self.binfreqs = {}
        for cat in self.data:
            self.binfreqs[cat] = [0 for i in range(self.nr_bins)]
            for x in self.data[cat]:
                for i in range(len(self.intervals)):
                    (min_x,max_x) = self.intervals[i]
                    if x >= min_x and x <= max_x:
                        freq = 1 + self.binfreqs[cat][i]
                        self.binfreqs[cat][i] = freq
                        max_freq = max(freq,max_freq)

        y_axis = Axis(self.height, "vertical", 0, max_freq, label="frequency")
        x_axis = Axis(self.width, "horizontal",x_min,x_max, label=str(self.x))
        self.setAxes(x_axis, y_axis)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def drawChart(self, doc, cx, cy, width, height):
        categories = {}
        for cat in self.binfreqs:
            colour = self.colour_manager.getColour(cat)
            binfreqs = self.binfreqs[cat]
            ids = []
            for index in range(len(self.intervals)):
                (lwb,upb) = self.intervals[index]
                freq = binfreqs[index]
                x0 = self.computeX(lwb)
                x1 = self.computeX(upb)
                y0 = self.computeY(0)
                y1 = self.computeY(freq)
                r = rectangle(x0,y1,(x1-x0),(y0-y1),fill=colour,stroke=self.stroke,stroke_width=self.stroke_width,tooltip=str(freq))
                ids.append(r.getId())
                doc.add(r)
            categories[cat] = ids
        return {"categories":categories}