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

from visigoth.svg import foreign_object
from visigoth.common.diagram_element import DiagramElement

class EmbeddedHtml(DiagramElement):
    """
    Create an embedded HTML with CSS

    Arguments:
        content_html(str): the HTML content as a string
        content_css(str): the CSS content as a string

    Keyword Arguments:
        width(int): width of the embedded HTML
        height(int): height of the embedded HTML
    """

    def __init__(self,content_html,content_css,width=512,height=512):
        DiagramElement.__init__(self)
        self.set_width = width
        self.set_height = height
        self.content_html = content_html
        self.content_css = content_css
        self.content_js = ""
        self.width = 0
        self.height = 0

    def substituteHtml(self,d):
        self.content_html = self.content_html%d

    def substituteCss(self,d):
        self.content_css = self.content_css%d

    def setHtml(self,html):
        self.content_html = html

    def setJs(self,js):
        self.content_js = js

    def build(self,fmt):
        super().build(fmt)
        if fmt != "html":
            self.width = 0
            self.height = 0
        else:
            self.width = self.set_width
            self.height = self.set_height

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def draw(self,d,cx,cy):
        if d.getFormat() != "html":
            return
        oy = cy - self.height/2
        ox = cx
        fo = foreign_object(self.width,self.height,ox-self.width/2,oy,self.content_html,self.content_css)
        d.add(fo)
        if self.content_js:
            d.addCode(self.content_js)
