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
from visigoth.map_layers.geoplot import Geoplot,Multipoint,Multiline
from collections import OrderedDict
from visigoth.utils.js import Js


class Network(MapLayer):
    """
    Create a Network plot

    Keyword Arguments:
        nodes(list) : a list of node objects
        edges(list) : a list of edge objects
        palette(DiscretePalette) : define the colours to use in conjunction with the ranking algorithm
        ranking_algorithm(object) : to colour nodes by rank, pass an instance of visigoth.map_layers.network.DDPageRank
        fill(str) : the default colour to use for filling nodes
        stroke(str) : the colour to use for contour lines
        stroke_width(float) : the width (in pixels) to use for contour lines
        font_height(int) : font size in pixels for contour labels
        text_attributes(dict): a dict containing SVG name/value attributes to apply to contour labels
    """
    def __init__(self,nodes=[],edges=[],ranking_algorithm=None,palette=None,fill="white",stroke="black",stroke_width=1,font_height=8,text_attributes={}):
        super(Network, self).__init__()
        self.nodes = nodes
        self.edges = edges
        self.palette = palette
        self.ranking_algorithm = ranking_algorithm
        self.width = None
        self.height = None
        self.projection = None
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.boundaries = None
        
    def getBoundaries(self):
        locations = [node.getLonLat() for node in self.nodes]
        if not self.boundaries:
            self.boundaries = Mapping.getBoundingBox(locations,0.05)
        return self.boundaries

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
        self.ownermap = ownermap
        self.width = width
        self.height = height
        self.boundaries = boundaries
        self.projection = projection
        self.height = height
        self.zoom_to = zoom_to
        
    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def build(self):
        ranks = {}
        if self.ranking_algorithm:
            ranks = self.ranking_algorithm.compute(self.nodes,self.edges,self.projection)
            min_rank = min([ranks[n] for n in ranks])
            max_rank = max([ranks[n] for n in ranks])
            self.palette.rescaleTo(min_rank,max_rank)
        mps = []
        for idx in range(len(self.nodes)):
            node = self.nodes[idx]
            if ranks:
                col = self.palette.getColour(ranks[idx])
            else:
                col = node.fill
            mps.append(Multipoint([node.getLonLat()],marker=False,tooltip=str(ranks[idx]),fill=col,stroke=node.stroke,stroke_width=node.stroke_width,radius=node.radius))
        
        mls = []
        for edge in self.edges:
            mls.append(Multiline([edge.getLonLats()],stroke=edge.stroke,stroke_width=edge.stroke_width))
        
        self.geoplot = Geoplot(multipoints=mps,multilines=mls)
        self.geoplot.configureLayer(self.ownermap,self.width,self.height,self.boundaries,self.projection,self.zoom_to)
        self.geoplot.build()

    def draw(self,doc,cx,cy):
        self.geoplot.draw(doc,cx,cy)
        with open(os.path.join(os.path.split(__file__)[0],"network.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc,self,jscode,"network",cx,cy,config)
        doc.getDiagram().connect(self,"zoom",self.geoplot,"zoom")
        doc.getDiagram().connect(self,"visible_window",self.geoplot,"visible_window")
