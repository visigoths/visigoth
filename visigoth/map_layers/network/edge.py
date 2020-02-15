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
