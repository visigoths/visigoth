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