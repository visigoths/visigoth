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