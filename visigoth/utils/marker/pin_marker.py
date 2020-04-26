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
from .marker import Marker

class PinMarker(Marker):

    svg = open(os.path.join(os.path.split(__file__)[0], "location_ionicon.svg"), "rt").read()

    def __init__(self, radius, stroke, stroke_width):
        super().__init__(radius,stroke,stroke_width)

    def plot(self, doc, x, y, tooltip, colour):
        r = self.getRadius()
        off_y = 32 * (2 * r / 512)
        i = embedded_svg(2 * r, 2 * r, x - r, y - 2 * r + off_y, PinMarker.svg)
        i.addAttr("fill", colour)
        i.addAttr("stroke", self.getStroke())
        i.addAttr("stroke-width", self.getStrokeWidth())
        if tooltip:
            i.setTooltip(tooltip)
        doc.add(i)
        return i.getId()


