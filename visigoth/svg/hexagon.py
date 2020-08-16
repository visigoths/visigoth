# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering geospatial information to SVG
#    Copyright (C) 2018  Niall McCarroll
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from visigoth.svg import polygon

import math

class hexagon(polygon):

    def __init__(self,x,y,dlength,fill,stroke,stroke_width):
        points = []
        off_lg = dlength*math.cos(math.radians(30))

        r = 0
        for idx in range(0,6):
            py = y+dlength*math.cos(r)
            px = x+dlength*math.sin(r)
            points.append((px,py))
            r += math.pi/3

        self.hexpoints = points
        super().__init__(points,fill,stroke,stroke_width)

    def getHexagonPoints(self):
        return self.hexpoints