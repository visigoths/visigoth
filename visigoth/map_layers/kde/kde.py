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
from collections import OrderedDict
from visigoth.utils.js import Js


class KDE(MapLayer):
    """
    Create a Kernel Density Estimate (KDE) plot
        data(list) : list of (lon,lat) datapoints

    Keyword Arguments:
        kernel: a kernel function mapping from distance in meters to a probability value
        bandwidth(int): defines the radius of the area of influence of each data point
        nr_samples_across(int): number of points to sample for contours across the plot
        contour_interval(float): height difference between contours
        palette(ContinuousPalette) : define the colours used in the plot
        stroke(str) : the colour to use for contour lines
        stroke_width(float) : the width (in pixels) to use for contour lines
        font_height(int) : font size in pixels for contour labels
        text_attributes(dict): a dict containing SVG name/value attributes to apply to contour labels
    """
    def __init__(self,data,kernel=None,bandwidth=1000,nr_samples_across=20,contour_interval=0.1,palette=None,label_fn=lambda x:"%.2f"%(x),stroke="brown",stroke_width=0,font_height=8,text_attributes={}):
        super(KDE, self).__init__()
        self.data = data
        self.kernel = kernel
        self.bandwidth = bandwidth
        self.palette = palette
        if self.kernel == None:
            self.kernel = KDE.createGaussianKernel(self.bandwidth)
        self.nr_samples_across = nr_samples_across
        self.width = None
        self.height = None
        self.projection = None
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.contour_interval = contour_interval
        self.label_fn = label_fn
        self.boundaries = None

    def getBoundaries(self):
        if not self.boundaries:
            self.boundaries = Mapping.getBoundingBox(self.data,0.05)
        return self.boundaries

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
        self.ownermap = ownermap
        self.width = width
        self.height = height
        self.boundaries = boundaries
        self.projection = projection
        (x0,y0) = projection.fromLonLat(boundaries[0])
        (x1,y1) = projection.fromLonLat(boundaries[1])
        self.height = height
        self.scale_x = self.width/(x1-x0)
        self.scale_y = self.height/(y1-y0)
        self.nr_samples_down = int(self.nr_samples_across * (self.height/self.width))
        self.zoom_to = zoom_to

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def build(self):
        tdata = []
        sw = self.boundaries[0]
        ne = self.boundaries[1]

        maxval = 0
        for row in range(0,self.nr_samples_down+1):
            yfrac = row / self.nr_samples_down
            tdata_row = []
            for column in range(0,self.nr_samples_across+1):
                xfrac = column / self.nr_samples_across
                lon = sw[0] + xfrac * (ne[0]-sw[0])
                lat = ne[1] + yfrac * (sw[1]-ne[1])
                (sx,sy) = self.projection.fromLonLat((lon,lat))
                val = 0
                for (loc_lon,loc_lat) in self.data:
                    (lx,ly) = self.projection.fromLonLat((loc_lon,loc_lat))
                    dist = math.sqrt((lx-sx)**2+(ly-sy)**2)
                    val += self.kernel(dist/self.bandwidth)
                val = val/(len(self.data)*self.bandwidth)
                if val > maxval:
                    maxval = val
                tdata_row.append(val)
            tdata.append(tdata_row)
        self.palette.rescaleTo(0.0,maxval)
        self.contour = Contour(tdata,maxval*0.1,palette=self.palette,label_fn=self.label_fn,stroke=self.stroke,stroke_width=self.stroke_width,font_height=self.font_height,text_attributes=self.text_attributes)
        self.contour.configureLayer(self.ownermap,self.width,self.height,self.boundaries,self.projection,self.zoom_to)
        self.contour.build()

    def draw(self,doc,cx,cy):
        self.contour.draw(doc,cx,cy)
        with open(os.path.join(os.path.split(__file__)[0],"kde.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc,self,jscode,"kde",cx,cy,config)
        doc.getDiagram().connect(self,"zoom",self.contour,"zoom")
        doc.getDiagram().connect(self,"visible_window",self.contour,"visible_window")

    @staticmethod
    def createUniformKernel(bandwidth):
        def kernelfn(dist):
            if dist > 1:
                return 0.0
            return 0.5
        return kernelfn

    @staticmethod
    def createGaussianKernel(bandwidth):
        def kernelfn(dist):
            return math.exp(-0.5*(dist**2))/math.sqrt(2*math.pi)
        return kernelfn
