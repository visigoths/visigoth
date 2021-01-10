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

import random
import sys
import json
import copy
import os
import os.path

from visigoth.map_layers.geoplot import Geoplot, Multipoint
from visigoth.utils.js import Js
from visigoth.utils.data import Dataset
from visigoth.utils.colour import DiscreteColourManager, ContinuousColourManager
from visigoth.utils.marker import MarkerManager
from visigoth.map_layers import MapLayer

class Scatter(Geoplot):

    """
    Create a Scatter plot

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)

    Keyword Arguments:
        lat (str or int): Identify the column to provide the latitude value for each point
        lon (str or int): Identify the column to provide the longitude value for each point
        colour (str or int): Identify the column to define the point colour (use colour_manager default colour if not specified)
        label (str or int): Identify the column to define the label
        size (str or int): Identify the column to determine the size of each marker
        colour_manager(object) : a ContinuousColourManager or DiscreteColourManager instance to control chart colour
        marker_manager(object) : a MarkerManager instance to control marker appearance
        marker (bool): plot a marker rather than circle
    """

    def __init__(self, data, lon=0, lat=1, colour=None, label=None, size=None, colour_manager=None, marker_manager=None):
        super().__init__()
        self.dataset = Dataset(data)

        self.lat = lat
        self.lon = lon
        self.colour = colour
        self.label = label
        self.size = size

        if not colour_manager:
            if not self.colour or self.dataset.isDiscrete(self.colour):
                colour_manager = DiscreteColourManager()
            else:
                colour_manager = ContinuousColourManager()
        self.setPalette(colour_manager)

        if not marker_manager:
            marker_manager = MarkerManager()
        self.setMarkerManager(marker_manager)

        self.data = self.dataset.query([self.lon, self.lat, self.label, self.colour, self.size])

        for (_,_,_,colour,size) in self.data:
            self.getMarkerManager().noteSize(size)
            self.getPalette().allocateColour(colour)

    def getBoundaries(self):
        return MapLayer.computeBoundaries(self.dataset.query([self.lon,self.lat]))

    def build(self,fmt):
        super().clear()
        for datapoint in self.data:
            point = (datapoint[0],datapoint[1])
            label = datapoint[2]
            col = datapoint[3]
            sz = datapoint[4]
            colour = self.colour_manager.getColour(col)
            marker = self.getMarkerManager().getMarker(sz)
            self.add(Multipoint([point],marker=marker,fill=colour,label=label))
        super().build(fmt)

    def draw(self,doc,cx,cy):
        config = super().draw(doc,cx,cy,False)
        with open(os.path.join(os.path.split(__file__)[0],"scatter.js"),"r") as jsfile:
            jscode = jsfile.read()
        # config = { "geoplot_id":self.getId() }
        Js.registerJs(doc,self,jscode,"scatter",cx,cy,config)
        # doc.getDiagram().connect(self,"zoom",self.geoplot,"zoom")
        # doc.getDiagram().connect(self,"visible_window",self.geoplot,"visible_window")
        

        
    