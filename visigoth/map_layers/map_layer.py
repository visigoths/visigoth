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

    def getOpacity(self):
        return self.opacity

    def setVisible(self,visible):
        self.visible = visible

    def getVisible(self):
        return self.visible

    def isForegroundLayer(self):
        return False

    