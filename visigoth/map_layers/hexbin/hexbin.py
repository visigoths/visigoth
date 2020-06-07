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
import urllib
import os
import json
import os.path

from visigoth.common import DiagramElement
from visigoth.common.image import Image
from visigoth.utils.mapping import Mapping
from visigoth.map_layers import MapLayer
from visigoth.map_layers.contour import Contour
from visigoth.svg import hexagon, circle
from visigoth.utils.js import Js

from visigoth.utils.data import Dataset

class Hexbin(MapLayer):
    """
    Create a Hexagonally binned plot of point density
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)

    Keyword Arguments:
        lat (str or int): Identify the column to provide the latitude value for each point
        lon (str or int): Identify the column to provide the longitude value for each point
        nr_bins_across: number of bins to arrange across the plot
        palette(ContinuousPalette) : define the colours used in the plot
        stroke(str) : the colour to use for bin lines
        stroke_width(float) : the width (in pixels) to use for bin lines
    """
    def __init__(self,data,lon=0,lat=1,nr_bins_across=10,palette=None,stroke="grey",stroke_width=1):
        super(Hexbin, self).__init__()
        dataset = Dataset(data)
        self.data = dataset.query([lon,lat])
        self.palette = palette
        self.nr_bins_across = nr_bins_across
        self.width = None
        self.height = None
        self.projection = None
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.bins = []
        self.boundaries = None

    def getBoundaries(self):
        if self.boundaries:
            return self.boundaries
        min_lon = min(map(lambda p:p[0],self.data))
        max_lon = max(map(lambda p:p[0],self.data))
        min_lat = min(map(lambda p:p[1],self.data))
        max_lat = max(map(lambda p:p[1],self.data))
        return ((min_lon,min_lat),(max_lon,max_lat))

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
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
        self.buildLayer()

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

    def buildLayer(self):
        for row in range(0,self.nr_bins_down):
            for col in range(0,self.nr_bins_across):
                self.centers[(col,row)] = self.hexacenter(col,row)
                self.freqs[(col,row)] = 0

        maxfreq = 0
        for point in self.data:
            (px,py) = self.transform(point)
            py = self.height - py
            self.points.append((px,py))
            for row in range(0,self.nr_bins_down):
                for col in range(0,self.nr_bins_across):
                    (hx,hy) = self.centers[(col,row)]
                    if self.inHexagon(px,py,hx,hy):
                        freq = self.freqs[(col,row)]+1
                        self.freqs[(col,row)] = freq
                        if freq > maxfreq:
                            maxfreq = freq

        self.palette.getColour(0)
        self.palette.getColour(maxfreq)

    def draw(self,doc,cx,cy):
        ox = cx - self.width/2
        oy = cy - self.height/2
        for row in range(0,self.nr_bins_down):
            for col in range(0,self.nr_bins_across):
                (hx,hy) = self.centers[(col,row)]
                freq = self.freqs[(col,row)]
                col = self.palette.getColour(freq)
                h = hexagon(ox+hx,oy+hy,self.dlength,col,self.stroke,self.stroke_width)
                doc.add(h)

        with open(os.path.join(os.path.split(__file__)[0],"hexbin.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc,self,jscode,"hexbin",cx,cy,config)
        