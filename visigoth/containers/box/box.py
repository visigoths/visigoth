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

from visigoth.common.diagram_element import DiagramElement
from visigoth.svg import rectangle

class Box(DiagramElement):

    """
    Wrap an element with a surrounding box

    Arguments:
        element(DiagramElement): element to wrap

    Keyword Arguments:
        margin(int): width of the margin in pixels
        stroke_width(int): width of the border in pixels
        stroke(str): colour of the border
        padding(int): width of the padding in pixels
        fill(str): fill colour for the box
    """
    def __init__(self,element,margin=2,stroke_width=2,stroke="grey",padding=2,fill=None):
        DiagramElement.__init__(self)
        self.element = element
        self.margin = margin
        self.stroke_width = stroke_width
        self.stroke = stroke
        self.padding = padding
        self.height = 0
        self.width = 0
        self.fill = fill
        self.element.setContainer(self)

    def build(self):
        self.element.build()

        self.width = self.margin*2+self.padding*2+self.stroke_width*2+self.element.getWidth()
        self.height = self.margin*2+self.stroke_width*2+self.padding*2+self.element.getHeight()

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def draw(self,diagram,cx,cy):
        y = cy - self.height/2
        x = cx

        ex = cx - self.width/2 + self.margin+self.stroke_width+self.padding+self.element.getWidth()/2
        ey = cy - self.height/2 + self.margin+self.stroke_width+self.padding+self.element.getHeight()/2

        if self.fill:
            diagram.add(rectangle(ex-self.element.getWidth()/2,ey-self.element.getHeight()/2,self.element.getWidth(),self.element.getHeight(),fill=self.fill))

        self.element.draw(diagram,ex,ey)

        if self.stroke_width and self.stroke:
            off_side = self.margin+self.stroke_width/2
            off_top = self.margin+self.stroke_width/2

            border_width = self.padding*2+self.element.getWidth()+self.stroke_width
            border_height = self.padding*2+self.element.getHeight()+self.stroke_width
            border = rectangle(x-self.width/2+off_side,y+off_top,border_width,border_height,stroke_width=self.stroke_width,stroke=self.stroke)
            diagram.add(border)


    def search(self,element_id):
        e = self.element.search(element_id)
        if e:
            return e
        
        return super(Switch,self).search(element_id)