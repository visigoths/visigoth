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

import os
import os.path
import math

from visigoth.utils.mapping import Mapping

from visigoth.map_layers.geoplot import Geoplot,Multipoint,Multiline
from visigoth.utils.js import Js
from visigoth.utils.colour import DiscretePalette, ContinuousPalette
from visigoth.utils.marker import MarkerManager
from visigoth.utils.data import Dataset

class Node(object):

    def __init__(self, lon, lat, label=None, size=None, colour=None):
        self.lon = lon
        self.lat = lat
        self.label = label
        self.size = size
        self.colour = colour

    def getLabel(self):
        return self.label

    def getSize(self):
        return self.size

    def getColour(self):
        return self.colour

    def getLonLat(self):
        return (self.lon, self.lat)


class Edge(object):

    def __init__(self, src_node, dest_node, width=None, colour=None):
        self.src_node = src_node
        self.dest_node = dest_node
        self.width = width
        self.colour = colour

    def getWidth(self):
        return self.width

    def getColour(self):
        return self.colour

    def getSrcNode(self):
        return self.src_node

    def getDestNode(self):
        return self.dest_node

    def getLonLats(self):
        return [self.src_node.getLonLat()] + [self.dest_node.getLonLat()]

    def getDistance(self, projection):
        ppoints = list(map(lambda x: projection.fromLonLat(x), self.getLonLats()))
        distance = 0
        for idx in range(1, len(ppoints)):
            (e1, n1) = ppoints[idx - 1]
            (e2, n2) = ppoints[idx]
            distance += math.sqrt((e1 - e2) ** 2 + (n1 - n2) ** 2)
        return distance


class Network(Geoplot):
    """
    Create a Network plot
        node_data (list): A relational data set (for example, list of dicts/lists/tuples describing each node)
        edge_data (list): A relational data set (for example, list of dicts/lists/tuples describing each edge)

    Keyword Arguments:
        node_id (str or int): Identify the column to provide the id value for each node
        node_lon (str or int): Identify the column to provide the longitude value for each node
        node_lat (str or int): Identify the column to provide the latitude value for each node
        node_label (str or int): Identify the column to provide the label for each node
        node_size (str or int): Identify the column to provide the size for each node

        edge_from_node (str or int): Identify the column to provide the id of the origin node for each edge
        edge_to_node (str or int): Identify the column to provide the id of the destination node for each edge

        ranking_algorithm(object) : to colour nodes by rank, pass an instance of visigoth.map_layers.network.DDPageRank

        palette(DiscretePalette) : define the colours to use in conjunction with the ranking algorithm
        marker_manager(MarkerManager) : manage the markers used to represent nodes

        font_height(int) : font size in pixels for contour labels
        text_attributes(dict): a dict containing SVG name/value attributes to apply to contour labels
    """
    def __init__(self,node_data,edge_data,node_id=0,node_lon=1,node_lat=2,node_label=None,node_size=None,edge_from_node=0,edge_to_node=1,ranking_algorithm=None,palette=None,marker_manager=None,font_height=8,text_attributes={}):
        super().__init__()
        node_dataset = Dataset(node_data)
        edge_dataset = Dataset(edge_data)
        nodes = node_dataset.query([node_id,node_lon,node_lat,node_label,node_size])
        edges = edge_dataset.query([edge_from_node,edge_to_node])
        nodes_by_id = {}

        self.nodes = []
        for (id,lon,lat,label,size) in nodes:
            node = Node(lon,lat,label=label,size=size)
            nodes_by_id[id] = node
            self.nodes.append(node)

        self.edges = []
        for (from_node,to_node) in edges:
            f = nodes_by_id[from_node]
            t = nodes_by_id[to_node]
            edge = Edge(f,t)
            self.edges.append(edge)

        if not palette:
            if self.colour is not None and self.dataset.isDiscrete(self.colour):
                palette = DiscretePalette()
            else:
                palette = ContinuousPalette()

        self.setPalette(palette)

        if not marker_manager:
            marker_manager = MarkerManager()
        self.setMarkerManager(marker_manager)

        self.ranking_algorithm = ranking_algorithm
        self.width = None
        self.height = None
        self.projection = None
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.boundaries = None
        
    def getBoundaries(self):
        locations = [node.getLonLat() for node in self.nodes]
        if not self.boundaries:
            self.boundaries = Mapping.getBoundingBox(locations,0.05)
        return self.boundaries

    def build(self):
        super().clear()
        ranks = {}
        if self.ranking_algorithm:
            ranks = self.ranking_algorithm.compute(self.nodes,self.edges,self.projection)
            min_rank = min([ranks[n] for n in ranks])
            max_rank = max([ranks[n] for n in ranks])
            self.palette.rescaleTo(min_rank,max_rank)

        for idx in range(len(self.nodes)):
            node = self.nodes[idx]
            if ranks:
                col = self.palette.getColour(ranks[idx])
            else:
                col = self.palette.getColour(node.getColour())
            marker = self.getMarkerManager().getMarker(node.getSize())
            self.add(Multipoint([node.getLonLat()],label=node.getLabel(),marker=marker,tooltip=str(ranks[idx]),fill=col))
        
        for edge in self.edges:
            self.add(Multiline([edge.getLonLats()],stroke="grey",stroke_width=3))
        
        super().build()

    def draw(self,doc,cx,cy):
        super().draw(doc,cx,cy)
        with open(os.path.join(os.path.split(__file__)[0],"network.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc,self,jscode,"network",cx,cy,config)
        # doc.getDiagram().connect(self,"zoom",self.geoplot,"zoom")
        # doc.getDiagram().connect(self,"visible_window",self.geoplot,"visible_window")
