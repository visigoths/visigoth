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

from visigoth.svg import embedded_svg
from visigoth.common.diagram_element import DiagramElement

class EmbeddedSvg(DiagramElement):
    """
    Create an embedded SVG

    Arguments:
        content(str): the SVG content as a string

    Keyword Arguments:
        width(int): width of the embedded SVG
        height(int): height of the embedded SVG
    """

    def __init__(self,content,width=512,height=512):
        DiagramElement.__init__(self)
        self.width = width
        self.height = height
        self.content = content

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def draw(self,d,cx,cy):
        oy = cy - self.height/2
        ox = cx
        es = embedded_svg(self.width,self.height,ox-self.width/2,oy,self.content)
        d.add(es)
