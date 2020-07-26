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

from visigoth.utils.data import Dataset

class Cluster(Geoplot):

    """
    Create a Cluster plot

    Arguments:
         data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)

    Keyword Arguments:
        algorithm: the algorithm to use (currently visigoth.map_layers.cluster.AgglomerativeAlgorithm or visigoth.map_layers.cluster.KMeansAlgorithm is supported)
        lat (str or int): Identify the column to provide the latitude value for each point
        lon (str or int): Identify the column to provide the longitude value for each point
        fill (tuple): tuple containing the colour for each center
        stroke (str): stroke colour for circles representing points
        stroke_width (int): stroke width for circles representing points
        radius (int): radius of circles representing points
        font_height(int) : font size in pixels for cluster labels (set to 0 to hide labels)
        text_attributes(dict): a dict containing SVG name/value attributes to apply to cluster labels
        label_fill(str): background colour to use for cluster labels
    """
    def __init__(self, data, algorithm,lon=0,lat=1,fill=[],stroke="black",stroke_width=1,radius=5,font_height=12,text_attributes={},label_fill="#B0B0B080"):
        super(Cluster, self).__init__(font_height=font_height,text_attributes=text_attributes)
        dataset = Dataset(data)
        self.data = dataset.query([lon,lat])
        self.algorithm = algorithm
  
        self.width = None
        self.height = None
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.radius = radius
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.label_fill = label_fill

    def getBoundaries(self):
        if not self.boundaries:
            boundaries = Mapping.getBoundingBox(self.data,0.05)
        return boundaries  

    def build(self,fmt):
        self.model = self.algorithm.train(self.data,self.projection)
        
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
            self.add(Multipoint(
                clusteredpoints[cluster],
                fill=colour,marker=False,radius=self.radius,stroke=self.stroke,stroke_width=self.stroke_width,
                **kwargs))
            
        super().build(fmt)

    def draw(self,doc,cx,cy):
        config = super().draw(doc,cx,cy,False)
        with open(os.path.join(os.path.split(__file__)[0],"cluster.js"),"r") as jsfile:
            jscode = jsfile.read()
        Js.registerJs(doc,self,jscode,"cluster",cx,cy,config)
        # doc.getDiagram().connect(self,"zoom",self.geoplot,"zoom")
        # doc.getDiagram().connect(self,"visible_window",self.geoplot,"visible_window")
