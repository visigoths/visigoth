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

import random
import sys
import json
import copy
import os
import os.path

from visigoth.map_layers.geoplot import Geoplot, Multipoint
from visigoth.utils.js import Js
from visigoth.utils.data import Dataset
from visigoth.utils.colour import DiscretePalette, ContinuousPalette
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
        colour (str or int): Identify the column to define the point colour (use palette default colour if not specified)
        label (str or int): Identify the column to define the label
        size (str or int): Identify the column to determine the size of each marker
        palette(object) : a ContinuousPalette or DiscretePalette instance to control chart colour
        marker_manager(object) : a MarkerManager instance to control marker appearance
        marker (bool): plot a marker rather than circle
    """

    def __init__(self, data, lon=0, lat=1, colour=None, label=None, size=None, palette=None, marker_manager=None):
        super().__init__()
        self.dataset = Dataset(data)

        self.lat = lat
        self.lon = lon
        self.colour = colour
        self.label = label
        self.size = size

        if not palette:
            if not self.colour or self.dataset.isDiscrete(self.colour):
                palette = DiscretePalette()
            else:
                palette = ContinuousPalette()
        self.setPalette(palette)

        if not marker_manager:
            marker_manager = MarkerManager()
        self.setMarkerManager(marker_manager)

        self.data = self.dataset.query([self.lon, self.lat, self.label, self.colour, self.size])

        for (_,_,_,colour,size) in self.data:
            self.getMarkerManager().noteSize(size)
            self.getPalette().getColour(colour)

    def getBoundaries(self):
        return MapLayer.computeBoundaries(self.dataset.query([self.lon,self.lat]))

    def build(self):
        super().clear()
        for datapoint in self.data:
            point = (datapoint[0],datapoint[1])
            label = datapoint[2]
            col = datapoint[3]
            sz = datapoint[4]
            colour = self.palette.getColour(col)
            marker = self.getMarkerManager().getMarker(sz)
            self.add(Multipoint([point],marker=marker,fill=colour,label=label))
        super().build()

    def draw(self,doc,cx,cy):
        config = super().draw(doc,cx,cy,False)
        with open(os.path.join(os.path.split(__file__)[0],"scatter.js"),"r") as jsfile:
            jscode = jsfile.read()
        # config = { "geoplot_id":self.getId() }
        Js.registerJs(doc,self,jscode,"scatter",cx,cy,config)
        # doc.getDiagram().connect(self,"zoom",self.geoplot,"zoom")
        # doc.getDiagram().connect(self,"visible_window",self.geoplot,"visible_window")
        

        
    