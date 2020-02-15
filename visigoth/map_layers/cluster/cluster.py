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
import math
import os.path

from math import radians,sin,cos,pi,sqrt,log

from visigoth.svg import polygon, circle, line, rectangle, clip_path
from visigoth.map_layers import MapLayer
from visigoth.map_layers.geoplot import Geoplot, Multipoint

from visigoth.containers.box import Box
from visigoth.utils.mapping import Mapping
from visigoth.utils.js import Js
from visigoth.utils.term.progress import Progress
from visigoth.utils.colour import Colour

class Cluster(MapLayer):

    """
    Create a Cluster plot

    Arguments:
        data(list) : list of (lon,lat) pairs to plot

    Keyword Arguments:
        algorithm: the algorithm to use (currently visigoth.map_layers.cluster.AgglomerativeAlgorithm or visigoth.map_layers.cluster.KMeansAlgorithm is supported)
        fill (tuple): tuple containing the colour for each center
        stroke (str): stroke colour for circles representing points
        stroke_width (int): stroke width for circles representing points
        radius (int): radius of circles representing points
        font_height(int) : font size in pixels for cluster labels (set to 0 to hide labels)
        text_attributes(dict): a dict containing SVG name/value attributes to apply to cluster labels
        label_fill(str): background colour to use for cluster labels
    """
    def __init__(self, data, algorithm,fill=[],stroke="black",stroke_width=1,radius=5,font_height=12,text_attributes={},label_fill="#B0B0B080"):
        super(Cluster, self).__init__()
        
        self.data  = data
        self.algorithm = algorithm
  
        self.width = None
        self.height = None
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.radius = radius
        self.points = []
        self.boundaries = None
        self.scale  = None
        self.projection = None
        self.geoplot = None
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.label_fill = label_fill
        

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
        self.ownermap = ownermap
        self.width = width
        self.height = height
        self.boundaries = boundaries
        self.projection = projection
        self.zoom_to = zoom_to

    def getBoundaries(self):
        if not self.boundaries:
            boundaries = Mapping.getBoundingBox(self.data,0.05)
        return boundaries  

    def getWidth(self):
        return self.geoplot.getWidth()

    def getHeight(self):
        return self.geoplot.getHeight()

    def build(self):
        self.model = self.algorithm.train(self.data,self.projection)
        
        multipoints = []
        cluster_colours = {idx:self.fill[idx] for idx in range(len(self.fill))}

        clusteredpoints = {}
        for point in self.data:
            cluster = self.model.score(point)
            clusterpoints = clusteredpoints.get(cluster,[])
            clusterpoints.append(point)
            clusteredpoints[cluster] = clusterpoints

        for cluster in clusteredpoints:
            label="cluster-%d"%(cluster)
            if cluster not in cluster_colours:
                cluster_colours[cluster] = Colour.randomColour()
            colour = cluster_colours[cluster]
            kwargs = {}
            if self.font_height>0:
                kwargs["label"] = label
            multipoints.append(Multipoint(
                clusteredpoints[cluster],
                fill=colour,marker=False,radius=self.radius,stroke=self.stroke,stroke_width=self.stroke_width,
                **kwargs))
            
        self.geoplot = Geoplot(multipoints=multipoints,font_height=self.font_height,text_attributes=self.text_attributes,label_fill=self.label_fill)
        self.geoplot.configureLayer(self.ownermap,self.width,self.height,self.boundaries,self.projection,self.zoom_to)
        self.geoplot.build()


    def draw(self,doc,cx,cy):
        self.geoplot.draw(doc,cx,cy)
        with open(os.path.join(os.path.split(__file__)[0],"cluster.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc,self,jscode,"cluster",cx,cy,config)
        doc.getDiagram().connect(self,"zoom",self.geoplot,"zoom")
        doc.getDiagram().connect(self,"visible_window",self.geoplot,"visible_window")
