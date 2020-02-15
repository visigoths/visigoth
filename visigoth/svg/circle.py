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

from visigoth.svg.svgstyled import svgstyled

# represent a circle as an SVG object
class circle(svgstyled):

    def __init__(self,x,y,r,fill="grey",tooltip="",stroke=None,stroke_width=None):
        svgstyled.__init__(self,'circle',tooltip)
        self.addAttr("cx",x).addAttr("cy",y).addAttr("r",r)
        if fill:
            self.addAttr("fill",fill)
        if stroke:
            self.addAttr("stroke",stroke)
        if stroke_width != None:
            self.addAttr("stroke-width",stroke_width)
