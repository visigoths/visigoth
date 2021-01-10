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

import math
import os
import os.path

from visigoth.utils.colour import ContinuousColourManager
from visigoth.map_layers import MapLayer
from visigoth.svg import hexagon
from visigoth.utils.js import Js
from visigoth.utils.term.progress import Progress

from visigoth.utils.data import Dataset

class Hexbin(MapLayer):
    """
    Create a Hexagonally binned plot of point density
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)

    Keyword Arguments:
        lat (str or int): Identify the column to provide the latitude value for each point
        lon (str or int): Identify the column to provide the longitude value for each point
        colour (float or int): Attach a magnitude value to each point (if None, all points are assigned a magnitude of 1)
        nr_bins_across: number of hexagonal bins to arrange across the plot
        colour_manager(ContinuousColourManager) : define the colours used in the plot
        stroke(str) : the colour to use for bin lines
        stroke_width(float) : the width (in pixels) to use for bin lines
        draw_empty_bins(bool) : whether to draw hexagonal bins with zero value
        min_freq(int) : only draw bins with this frequency or higher
    """
    def __init__(self,data,lon=0,lat=1,colour=None,nr_bins_across=10,colour_manager=None,stroke="grey",stroke_width=1, draw_empty_bins=False,min_freq=1):
        super(Hexbin, self).__init__()
        dataset = Dataset(data)
        self.data = dataset.query([lon,lat,colour if colour is not None else Dataset.constant(1)])
        if colour_manager == None:
            colour_manager = ContinuousColourManager()
        self.setPalette(colour_manager)
        self.nr_bins_across = nr_bins_across
        self.width = None
        self.height = None
        self.projection = None
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.bins = []
        self.boundaries = None
        self.draw_empty_bins = draw_empty_bins
        self.min_freq = min_freq

    def getBoundaries(self):
        if self.boundaries:
            return self.boundaries
        min_lon = min(map(lambda p:p[0],self.data))
        max_lon = max(map(lambda p:p[0],self.data))
        min_lat = min(map(lambda p:p[1],self.data))
        max_lat = max(map(lambda p:p[1],self.data))
        return ((min_lon,min_lat),(max_lon,max_lat))

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to,fmt):
        self.width = width
        self.height = height
        self.ownermap = ownermap
        self.boundaries = boundaries
        self.projection = projection
        (x0,y0) = projection.fromLonLat(boundaries[0])
        (x1,y1) = projection.fromLonLat(boundaries[1])
        self.se = (x0,y0)
        self.nw = (x1,y1)
        self.scale_x = self.width/(x1-x0)
        self.scale_y = self.height/(y1-y0)
        self.nr_bins_down = int(self.nr_bins_across * (self.height/self.width))
        self.rangle = math.radians(30)
        self.dlength = (self.width)/(2*math.cos(self.rangle) * (self.nr_bins_across-1))
        self.nr_bins_down = 1+int((self.height)/(self.dlength*(1+math.sin(self.rangle))))

        self.spacing = 2*self.dlength * math.sin(self.rangle)
        self.centers = {}
        self.freqs = {}
        self.points = []
        self.buildLayer(fmt)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def hexacenter(self,col,row):
        off_sm = self.dlength*math.sin(self.rangle)
        off_lg = self.dlength*math.cos(self.rangle)
        yc = (float(row)*(self.dlength+off_sm))+off_sm
        xc = (float(col)*(2*off_lg))
        if row % 2 == 1:
            xc += off_lg
        return (xc,yc)

    def transform(self,point):
        (px1,py1) = self.projection.fromLonLat(point)
        px = (px1 - self.se[0])*self.scale_x
        py = (py1 - self.se[1])*self.scale_y
        return (px,py)

    def inHexagon(self,px,py,hx,hy):
        s = self.dlength
        x = abs(px - hx)
        y = abs(py - hy)
        return x < 3**0.5 * min(s - y, s / 2)

    def buildLayer(self,fmt):
        for row in range(0,self.nr_bins_down):
            for col in range(0,self.nr_bins_across):
                self.centers[(col,row)] = self.hexacenter(col,row)
                self.freqs[(col,row)] = 0

        progress = Progress("hexbin")
        maxfreq = 0
        count = 0
        total = len(self.data)
        for (lon,lat,value) in self.data:
            (px,py) = self.transform((lon,lat))
            py = self.height - py
            self.points.append((px,py))
            col_e = (px / self.width) * self.nr_bins_across
            row_e = (py / self.height) * self.nr_bins_down
            row_min = max(math.floor(row_e-1),0)
            row_max = min(math.ceil(row_e+1),self.nr_bins_down-1)
            col_min = max(math.floor(col_e - 1), 0)
            col_max = min(math.ceil(col_e + 1), self.nr_bins_across-1)
            hits = 0
            for row in range(row_min,row_max+1):
                for col in range(col_min,col_max+1):
                    (hx,hy) = self.centers[(col,row)]
                    if self.inHexagon(px,py,hx,hy):
                        hits += 1
                        freq = self.freqs[(col,row)]+value
                        self.freqs[(col,row)] = freq
                        if freq > maxfreq:
                            maxfreq = freq
            count += 1
            progress.report("building",(count+1)/total)
        progress.complete("complete")
        self.getPalette().allocateColour(0)
        self.getPalette().allocateColour(maxfreq)
        self.getPalette().build()

    def draw(self,doc,cx,cy):
        ox = cx - self.width/2
        oy = cy - self.height/2
        for row in range(0,self.nr_bins_down):
            for col in range(0,self.nr_bins_across):
                (hx,hy) = self.centers[(col,row)]
                freq = self.freqs[(col,row)]
                if freq>=self.min_freq or self.draw_empty_bins:
                    col = self.getPalette().getColour(freq)
                    h = hexagon(ox+hx,oy+hy,self.dlength,col,self.stroke,self.stroke_width)
                    doc.add(h)

        with open(os.path.join(os.path.split(__file__)[0],"hexbin.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc,self,jscode,"hexbin",cx,cy,config)
        