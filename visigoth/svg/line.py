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

class line(svgstyled):

    def __init__(self,x1,y1,x2,y2,stroke="black",stroke_width=2,tooltip=""):
        svgstyled.__init__(self,'line',tooltip)
        self.addAttr("x1",x1)
        self.addAttr("y1",y1)
        self.addAttr("x2",x2)
        self.addAttr("y2",y2)
        self.addAttr("stroke",stroke)
        self.addAttr("stroke-width",stroke_width)