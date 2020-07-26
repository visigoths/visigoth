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

from xml.dom.minidom import *

from visigoth.svg.svgstyled import svgstyled

class foreign_object(svgstyled):

    def __init__(self,width,height,x,y,content_html,content_css):
        svgstyled.__init__(self,'foreignObject',"")
        self.addAttr("width",width)
        self.addAttr("height",height)
        self.addAttr("x",x)
        self.addAttr("y",y)
        self.content_str = "<style>"+content_css+"</style>" + "<body style=\"height:100%;overflow:auto;\">"+content_html+"</body>"

    def render(self, svgdoc, parent):
        fo = super().render(svgdoc,parent)
        marker = svgdoc.getMarker(self.content_str)
        fo.appendChild(svgdoc.doc.createTextNode(marker))
        return fo