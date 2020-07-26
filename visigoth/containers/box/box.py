# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#   and associated documentation files (the "Software"), to deal in the Software without
#   restriction, including without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or
#   substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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

    def build(self,fmt):
        self.element.build(fmt)

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