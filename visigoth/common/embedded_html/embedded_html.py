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
        self.width = width
        self.height = height
        self.content_html = content_html
        self.content_css = content_css

    def substituteHtml(self,d):
        self.content_html = self.content_html%d

    def substituteCss(self,d):
        self.content_css = self.content_css%d

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def draw(self,d,cx,cy):
        oy = cy - self.height/2
        ox = cx
        fo = foreign_object(self.width,self.height,ox-self.width/2,oy,self.content_html,self.content_css)
        d.add(fo)
