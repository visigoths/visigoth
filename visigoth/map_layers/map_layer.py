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
        self.palette = None
        self.marker_manager = None

    def setPalette(self, palette):
        self.palette = palette
        return self

    def getPalette(self):
        return self.palette

    def setMarkerManager(self, marker_manager):
        self.marker_manager = marker_manager
        return self

    def getMarkerManager(self):
        return self.marker_manager

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
        pass

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

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
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
        nw = self.projection.fromLonLat(self.boundaries[0])

        cx = ox + (x - nw[0]) * self.scale_x
        cy = oy + (self.height - (y - nw[1]) * self.scale_y)
        return (cx,cy)

