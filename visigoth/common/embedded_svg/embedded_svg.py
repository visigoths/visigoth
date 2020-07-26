# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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
