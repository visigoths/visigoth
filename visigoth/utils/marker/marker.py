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

import os.path
from visigoth.svg import embedded_svg

class Marker(object):

    def __init__(self, radius, stroke, stroke_width):
        self.radius = radius
        self.stroke = stroke
        self.stroke_width = stroke_width

    def getRadius(self):
        return self.radius

    def getStroke(self):
        return self.stroke

    def getStrokeWidth(self):
        return self.stroke_width

    def plot(self, doc, x, y, tooltip, colour):
        raise NotImplementedError("plot")


