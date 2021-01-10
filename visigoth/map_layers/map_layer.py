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

from visigoth.common import DiagramElement
from visigoth.utils.mapping import Metadata

class MapLayer(DiagramElement):

    counter = 0

    """
    Superclass of all map layers
    """

    def __init__(self,metadata=None):
        super(MapLayer, self).__init__()
        if metadata:
            self.metadata = metadata
        else:
            self.metadata = Metadata()
        MapLayer.counter += 1
        self.opacity = 1.0
        self.visible = True
        self.colour_manager = None
        self.marker_manager = None

    def setPalette(self, colour_manager):
        self.colour_manager = colour_manager
        return self

    def getPalette(self):
        return self.colour_manager

    def setMarkerManager(self, marker_manager):
        self.marker_manager = marker_manager
        return self

    def getMarkerManager(self):
        return self.marker_manager

    def isSearchable(self):
        return False

    def getBoundaries(self):
        pass

    def getMetadata(self):
        return self.metadata

    def setInfo(self,name,description="",attribution="",url=""):
        self.metadata.setDetails(name,description,attribution,url)
        return self

    def setOpacity(self,opacity):
        self.opacity = opacity
        return self

    def getOpacity(self):
        return self.opacity

    def setVisible(self,visible):
        self.visible = visible
        return self

    def getVisible(self):
        return self.visible

    def isForegroundLayer(self):
        return False

    def build(self,fmt):
        if self.colour_manager:
            self.colour_manager.build()

    @staticmethod
    def computeBoundaries(locations):
        min_lon = None
        min_lat = None
        max_lon = None
        max_lat = None
        for (lon,lat) in locations:
            if min_lon == None or lon < min_lon:
                min_lon = lon
            if min_lat == None or lat < min_lat:
                min_lat = lat
            if max_lon == None or lon > max_lon:
                max_lon = lon
            if max_lat == None or lat > max_lat:
                max_lat = lat
        return ((min_lon, min_lat), (max_lon, max_lat))

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to,fmt):
        self.width = width
        self.boundaries = boundaries
        self.projection = projection
        (self.x0, self.y0) = self.projection.fromLonLat(boundaries[0])
        (self.x1, self.y1) = self.projection.fromLonLat(boundaries[1])
        self.height = height
        self.scale_x = self.width / (self.x1 - self.x0)
        self.scale_y = self.height / (self.y1 - self.y0)

    def drawTo(self,cx,cy):
        self.center_x = cx
        self.center_y = cy

    def getXYFromLonLat(self,lon_lat):
        (lon,lat) = lon_lat
        (x, y) = self.projection.fromLonLat((lon, lat))
        return self.getXY((x,y))

    def getXY(self,e_n):
        (x,y) = e_n
        ox = self.center_x - self.width/2
        oy = self.center_y - self.height/2
        on = self.projection.fromLonLat(self.boundaries[1])[1]
        oe = self.projection.fromLonLat(self.boundaries[0])[0]
        cx = ox + (x - oe) * self.scale_x
        cy = oy + (on - y) * self.scale_y
        return (cx,cy)

