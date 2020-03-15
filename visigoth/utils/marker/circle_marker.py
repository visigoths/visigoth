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

from visigoth.svg import circle

class CircleMarker(object):

    def __init__(self,radius,stroke,stroke_width):
        self.radius = radius
        self.stroke = stroke
        self.stroke_width = stroke_width

    def plot(self,doc,x,y,tooltip,colour):
        circ = circle(x,y,self.radius,colour,tooltip=tooltip)
        circ.addAttr("stroke",self.stroke)
        circ.addAttr("stroke-width",self.stroke_width)
        doc.add(circ)
        return circ.getId()

    
        