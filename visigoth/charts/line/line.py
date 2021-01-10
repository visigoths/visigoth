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

from visigoth.svg import path
from visigoth.common.axis import Axis
from visigoth.utils.data import Dataset
from visigoth.utils.marker import MarkerManager
from visigoth.utils.colour import DiscreteColourManager, ContinuousColourManager

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
        colour_manager(object) : a ContinuousColourManager or DiscreteColourManager instance to control line colour
        marker_manager(object) : a MarkerManager instance to control marker appearance
        smoothing (float) : smoothing factor to apply to lines, 0.0=no smoothing
        line_width (int) : specify the width of the lines in pixels
        font_height (int): the height of the font for text labels
        text_attributes (dict): SVG attribute name value pairs to apply to labels

    Note:
        None values are permitted in some data values with the following effect:
            y: point not plotted, line will be broken
            size: point assigned default size
            colour: points assigned default colour

    """

    def __init__(self, data,x=0,y=1,id=None,colour=None,label=None,size=None,width=768, height=768, colour_manager=None, marker_manager=None, smoothing=0.0, line_width=2, font_height=24, text_attributes={}):
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
        
        if not colour_manager:
            if self.colour == None or self.dataset.isDiscrete(self.colour):
                colour_manager = DiscreteColourManager()
            else:
                colour_manager = ContinuousColourManager()
        self.setPalette(colour_manager)

        if not marker_manager:
            marker_manager = MarkerManager()
        self.setMarkerManager(marker_manager)
        
        self.smoothing = smoothing
        self.line_width = line_width
        
        self.font_height = font_height
        self.text_attributes = text_attributes

        if len(self.dataset) > 0:
            xy_range = self.dataset.query(aggregations=[Dataset.min(self.x),Dataset.max(self.x),Dataset.min(self.y),Dataset.max(self.y)])[0]
            empty_x_count = self.dataset.query(aggregations=[Dataset.count_none(self.x)], flatten=True)[0]
            if empty_x_count > 0:
                raise Exception("x column cannot contain missing/None values")
        else:
            xy_range = (0.0,1.0,0.0,1.0)
        (x_axis_min,x_axis_max,y_axis_min,y_axis_max) = tuple(xy_range)

        x_label = "X"
        y_label = "Y"
        if isinstance(self.x,str):
            x_label = self.x
        if isinstance(self.y,str):
            y_label = self.y

        if self.colour != None:
            for val in self.dataset.query([self.colour],unique=True,flatten=True):
                self.getPalette().allocateColour(val)

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
            if x is not None and y is not None:
                cx = self.computeX(x)
                cy = self.computeY(y)

                marker = self.getMarkerManager().getMarker(sz)
                cid = marker.plot(doc,cx,cy,self.getTooltip(cat,(x,y)),col)

                if cat is not None:
                    ids = categories.get(cat,[])
                    ids.append(cid)
                    categories[cat] = ids
            
        def plotline(linepoints,linecat):
            if not linepoints:
                return
            linepoints = sorted(linepoints,key=lambda p:p[0])
            coords = []
            if linecat is not None:
                col = self.colour_manager.getColour(linecat)
            else:
                col = self.colour_manager.getDefaultColour()

            for idx in range(len(linepoints)):
                (x,y,_) = linepoints[idx]
                if x is not None and y is not None:
                    coords.append((self.computeX(x),self.computeY(y)))
                if x is None or y is None or idx==len(linepoints)-1:
                    # draw the line segment if more than 1 point is collected
                    # and we've reached either a missing x/y value or the end of the line
                    if len(coords) > 1:
                        p = path(coords,col,self.line_width,smoothing=self.smoothing)
                        ids = categories.get(linecat,[])
                        ids.append(p.getId())
                        if linecat is not None:
                            categories[linecat] = ids
                        doc.add(p)
                    coords = []

            for (x,y,sz) in linepoints:
                plotpoint(x,y,linecat,col,sz)

        if self.colour != None:
            linecats = map(lambda x:x[0],self.dataset.query([self.colour],unique=True))
            for linecat in linecats:
                linepoints = self.dataset.query([self.x,self.y,self.size],filters=[self.dataset.filter(self.colour,"=",linecat)])
                plotline(linepoints,linecat)
        else:
            linepoints = self.dataset.query([self.x,self.y,self.size])
            plotline(linepoints,None)

        return {"categories":categories}