# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

from visigoth.utils.marker.circle_marker import CircleMarker

class MarkerManager(object):

    def __init__(self,min_radius=1,max_radius=10):
        self.min_radius = min_radius
        self.max_radius = max_radius
        self.size_min = None
        self.size_max = None

    def noteSize(self,size):
        if self.size_min is None or size < self.size_min:
            self.size_min = size
        if self.size_max is None or size > self.size_max:
            self.size_max = size
        
    def getMarker(self,size,default_radius):
        if size is None or self.size_max is None:
            r = default_radius
        else:
            r = self.min_radius + (self.max_radius-self.min_radius)*(size/self.size_max)
        return CircleMarker(r)
        