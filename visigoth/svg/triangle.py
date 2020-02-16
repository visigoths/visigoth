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

from visigoth.svg import polygon

import math

class triangle(polygon):

    def __init__(self,cx,cy,radius,angle,fill="none",stroke="black",stroke_width=0):
        points = []
        for idx in range(3):
            a = angle + (idx*math.pi*2.0/3.0)
            x = cx+radius*math.sin(a)
            y = cy+radius*math.cos(a)
            points.append((x,y))
        super(triangle,self).__init__(points,fill,stroke,stroke_width)