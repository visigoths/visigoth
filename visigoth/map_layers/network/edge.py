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

class Edge(object):

    def __init__(self,src_node,dest_node,waypoints=[],stroke="black",stroke_width=3):
        self.src_node = src_node
        self.dest_node = dest_node
        self.waypoints = waypoints
        self.stroke = stroke
        self.stroke_width = stroke_width
        
    def getSrcNode(self):
        return self.src_node

    def getDestNode(self):
        return self.dest_node

    def getLonLats(self):
        return [self.src_node.getLonLat()] + self.waypoints + [self.dest_node.getLonLat()]

    def getDistance(self,projection):
        ppoints = list(map(lambda x: projection.fromLonLat(x),self.getLonLats()))
        distance = 0
        for idx in range(1,len(ppoints)):
            (e1,n1) = ppoints[idx-1]
            (e2,n2) = ppoints[idx]
            distance += math.sqrt((e1-e2)**2 + (n1-n2)**2)
        return distance
