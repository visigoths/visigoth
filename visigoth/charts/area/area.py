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
from visigoth.common import Axis
from visigoth.utils.colour.colour_manager import DiscreteColourManager
from visigoth.utils.data import Dataset
from visigoth.utils.marker import MarkerManager

class Area(ChartElement):

    """
    Create a stacked area plot

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each point)
        
    Keyword Arguments:
        x (str or int): Identify the column to specify x-axis point value
        y (str or int): Identify the column to specify y-axis point value.  Y values should be positive.
        colour (str or int): Identify the column to define the area and colour 
        id (str or int): Identify the column to define the unique id of each point
        label (str or int): Identify the column to define the label of each point
        size (str or int): Identify the column to determine the size of each point
        width(int) : the width of the plot including axes
        height(int) : the height of the plot including axes
        colour_manager(object) : a ContinuousColourManager or DiscreteColourManager instance to control line colour
        marker_manager(object) : a MarkerManager instance to control marker appearance
        smoothing (float) : smoothing factor to apply to lines, 0.0=no smoothing
        line_width (int) : width of the lines
        font_height (int): the height of the font for text labels
        text_attributes (dict): SVG attribute name value pairs to apply to labels
    """

    def __init__(self, data, x=0, y=1, colour=2, id=None, label=None, size=None, width=768, height=768,  colour_manager=None, marker_manager=None, smoothing=0.0, line_width=4, font_height=24, text_attributes={}):
        super(Area, self).__init__()
        self.setTooltipFunction(lambda cat,val: "%s: (%s,%s)"%(cat,str(val[0]),str(val[1])))
        self.setDrawGrid(True)
        self.x = x
        self.y = y
        self.colour = colour
        self.id = id
        self.label = label
        self.size = size

        self.data = Dataset(data)

        self.xcs = sorted(self.data.query([self.x],unique=True,flatten=True))
        if self.colour:
            self.cats = self.data.query([self.colour],unique=True,flatten=True)
        else:
            self.cats = []

        self.width = width
        self.height = height
    
        if not colour_manager:
            colour_manager = DiscreteColourManager()
        for cat in self.cats:
            colour_manager.allocateColour(cat)
        self.setPalette(colour_manager)

        if not marker_manager:
            marker_manager = MarkerManager()
        self.setMarkerManager(marker_manager)
       
        self.smoothing = smoothing
        self.line_width = line_width
        
        self.font_height = font_height
        self.text_attributes = text_attributes
        
        self.catmap = {} # mapping from colour-category to list of SVG ids

        if len(self.data) > 0:
            x_range = self.data.query(
                aggregations=[Dataset.min(self.x), Dataset.max(self.x)])[0]
        else:
            x_range = (0.0, 1.0)

        (x_axis_min, x_axis_max) = tuple(x_range)

        if len(self.data) > 0:
            y_range = self.data.query(
                columns=[self.x],
                aggregations=[Dataset.sum(self.y)]
            )
            y_axis_max = max([y for [_,y] in y_range])
        else:
            y_axis_max = 1.0
        # always start the y-axis at 0 to correctly represent areas
        y_axis_min = 0

        x_label = "X"
        y_label = "Y"
        if isinstance(self.x,str):
            x_label = self.x
        if isinstance(self.y,str):
            y_label = self.y

        if self.colour != None:
            for val in self.data.query([self.colour],unique=True,flatten=True):
                self.getPalette().allocateColour(val)
        
        if self.size != None:
            for v in self.data.query([self.size],unique=True,flatten=True):
                self.getMarkerManager().noteSize(v)

        ax = Axis(self.width,"horizontal",x_axis_min,x_axis_max,label=x_label,font_height=self.font_height,text_attributes=self.text_attributes)
        ay = Axis(self.height,"vertical",y_axis_min,y_axis_max,label=y_label,font_height=self.font_height,text_attributes=self.text_attributes)
        self.setAxes(ax,ay)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def plotPoint(self,diagram,cat,x,y,col,sz):
        cx = self.computeX(x)
        cy = self.computeY(y)
        marker = self.marker_manager.getMarker(sz)
        cid = marker.plot(diagram,cx,cy,self.getTooltip(cat,(x,y)),col)

        if cat:
            ids = self.catmap.get(cat,[])
            ids.append(cid)
            self.catmap[cat] = ids
        
    def plotLine(self,diagram,cat,linepoints,col):
        if not linepoints:
            return

        coords = [(self.computeX(x),self.computeY(y)) for (x,y,_) in linepoints]

        p = path(coords,col,self.line_width,smoothing=self.smoothing)

        p.close([(self.computeX(self.getXRange()[1]),self.computeY(0)),(self.computeX(self.getXRange()[0]),self.computeY(0))])
        p.addAttr("fill",col)
    
        if cat:
            ids = self.catmap.get(cat,[])
            ids.append(p.getId())
            self.catmap[cat] = ids

        diagram.add(p)

        for (x,y,sz) in linepoints:
            self.plotPoint(diagram,cat,x,y,col,sz)

    def drawArea(self,diagram):
        points = self.data.query([self.x,self.y,self.id,self.label,self.size])
        linepoints = [(x,y,sz) for (x,y,_,_,sz) in points]
        linepoints = sorted(linepoints,key=lambda p:p[0])
        self.plotLine(diagram,None,linepoints,self.colour_manager.getDefaultColour())
            
    def drawAreas(self,diagram):
    
        catlines = {}
        catdata = {}

        for cat in self.cats:
            catdata[cat] = self.data.query([self.x,self.y,self.id,self.label,self.size],filters=[Dataset.filter(self.colour,"=",cat)])

        for x in self.xcs:
            yc = 0
            
            for cat in self.cats:
                points = catdata[cat]
                point = [(py,id,label,sz) for (px,py,id,label,sz) in points if px==x]
                if not point:
                    raise Exception("Invalid input data")
                else:
                    point = point[0]

                yc += point[0]
                sz = point[3]
                    
                line = catlines.get(cat,[])
                line.append((x,yc,sz))
                catlines[cat] = line

        revcats = self.cats
        revcats.reverse()
        for cat in revcats:
            linepoints = catlines[cat]
            linepoints = sorted(linepoints,key=lambda p:p[0])
            linecol = self.colour_manager.getColour(cat)
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