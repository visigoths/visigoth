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
from visigoth.utils.data import Dataset
from visigoth.utils.colour import DiscretePalette, ContinuousPalette

from visigoth.common.axis import Axis
from visigoth.utils.marker import MarkerManager

class Scatter(ChartElement):

    """
    Create a Scatter plot

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)
    
    Keyword Arguments:
        x (str or int): Identify the column to provide the x-axis value for each point
        y (str or int): Identify the column to provide the y-axis value for each point
        width(int) : the width of the plot including axes
        height(int) : the height of the plot including axes
        colour (str or int): Identify the column to define the point colour (use palette default colour if not specified)
        label (str or int): Identify the column to define the label
        size (str or int): Identify the column to determine the size of each marker
        palette(object) : a ContinuousPalette or DiscretePalette instance to control chart colour
        marker_manager(object) : a MarkerManager instance to control marker appearance
        font_height (int): the height of the font for text labels
        text_attributes (dict): SVG attribute name value pairs to apply to labels
    """

    def __init__(self, data, x=0, y=1, width=768, height=768, colour=None, label=None, size=None, palette=None, marker_manager=None, font_height=24, text_attributes={}):
        super(Scatter, self).__init__()
        self.setTooltipFunction(lambda cat,val: "%s %s: (%.02f,%.02f)"%(cat[0],cat[1],val[0],val[1]))
        self.dataset = Dataset(data)
        self.setDrawGrid(True)
        self.x = x
        self.y = y
        self.colour = colour
        self.size = size
        self.label = label

        self.width = width
        self.height = height
        
        if not palette:
            if not self.colour or self.dataset.isDiscrete(self.colour):
                palette = DiscretePalette()
            else:
                palette = ContinuousPalette()
        self.setPalette(palette)

        if not marker_manager:
            marker_manager = MarkerManager()
        self.setMarkerManager(marker_manager)

        self.font_height = font_height
        self.text_attributes = text_attributes

        if len(self.dataset) > 0:
            xy_range = self.dataset.query(aggregations=[Dataset.min(self.x),Dataset.max(self.x),Dataset.min(self.y),Dataset.max(self.y)])[0]
        else:
            xy_range = [0.0,1.0,0.0,1.0]
        (x_axis_min,x_axis_max,y_axis_min,y_axis_max) = tuple(xy_range)

        x_label = "X"
        y_label = "Y"
        if isinstance(self.x,str):
            x_label = self.x
        if isinstance(self.y,str):
            y_label = self.y

        ax = Axis(self.width,"horizontal",x_axis_min,x_axis_max,label=x_label,font_height=self.font_height,text_attributes=self.text_attributes)
        ay = Axis(self.height,"vertical",y_axis_min,y_axis_max,label=y_label,font_height=self.font_height,text_attributes=self.text_attributes)
        
        self.setAxes(ax,ay)
        if self.colour:
            for v in self.dataset.query([self.colour],unique=True,flatten=True):
                self.getPalette().getColour(v)
        if self.size:
            for v in self.dataset.query([self.size],unique=True,flatten=True):
                self.getMarkerManager().noteSize(v)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def drawChart(self,doc,chart_cx,chart_cy,chart_width,chart_height):        
        
        categories = {}
        def plot(doc,x,y,v,label,sz):
            if v != None:
                col = self.palette.getColour(v)
            else:
                col = self.palette.getDefaultColour()

            cx = self.computeX(x)
            cy = self.computeY(y)

            marker = self.getMarkerManager().getMarker(sz)
            return marker.plot(doc,cx,cy,self.getTooltip((label,v),(x,y)),col)

        for (x,y,label,v,sz) in self.dataset.query([self.x,self.y,self.label,self.colour,self.size]):
            cid = plot(doc,x,y,v,label,sz)
            if v:
                ids = categories.get(v,[])
                ids.append(cid)
                categories[v] = ids

        return {"categories":categories}