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
import urllib
import os
import json

from visigoth.common import DiagramElement
from visigoth.common.image import Image
from visigoth.utils.mapping import Mapping
from visigoth.map_layers import MapLayer
from visigoth.map_layers.geoplot import Geoplot,Multipoint,Multiline
from collections import OrderedDict

class DDPageRank(object):
    """
    Rank nodes according to a distance decay page rank model

    Keyword Arguments:
        num_iters(int) : number of iterations to use
        damping(float) : damping factor between 0.0 and 1.0
        
    """
    def __init__(self,num_iters=100,damping=0.85):
        self.num_iters = num_iters
        self.damping = damping
        self.distances = {} # src-node -> dest-node -> [distances]

    def trackDistances(self,src,dest,dist):
        srcmap = self.distances.get(src,{})
        destlist = srcmap.get(dest,[])
        destlist.append(dist)
        srcmap[dest] = destlist
        self.distances[src] = srcmap
            
    def compute(self,nodes,edges,projection):
        self.distances = {}
        for edge in edges:
            el = edge.getDistance(projection)
            s = nodes.index(edge.getSrcNode())
            d = nodes.index(edge.getDestNode())
            self.trackDistances(s,d,el)
            self.trackDistances(d,s,el)

        for n in range(0,len(nodes)):
            if n not in self.distances:
                self.distances[n] = {}

        ranks = {i:1.0/float(len(nodes)) for i in range(len(nodes))}

        for iter in range(0,self.num_iters):
            nextranks = {i:(1.0-self.damping)/float(len(nodes)) for i in range(len(nodes))}
            for n in range(0,len(nodes)):
                links = self.distances[n]
                totalinvdist = 0.0
                for to in links:
                    for dist in links[to]:
                        totalinvdist += 1/dist
                for to in links:
                    for dist in links[to]:
                        invdist = 1/dist
                        nextranks[to] = nextranks[to] + self.damping * ranks[n] * (invdist/totalinvdist)
            ranks = nextranks

        return ranks