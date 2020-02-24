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

# represent a line with a cubic bezier curve as an SVG object
class cubic_bezier(svgstyled):

    def __init__(self,p1,cp1,cp2,p2,stroke,stroke_width,tooltip=""):
        svgstyled.__init__(self,"path",tooltip)
        self.addAttr("d",self.computePath(p1,cp1,cp2,p2))
        self.addAttr("fill","none")
        if stroke and stroke_width:
            self.addAttr("stroke-width",stroke_width).addAttr("stroke",stroke)

    def addPoint(self,p):
        return str(p[0]) + "," + str(p[1])

    def computePath(self,p1,cp1,cp2,p2):
        s = "M"+self.addPoint(p1)
        s += " C"+self.addPoint(cp1)
        s += " "+self.addPoint(cp2)
        s += " "+self.addPoint(p2)
        return s

