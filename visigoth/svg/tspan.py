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
from math import cos,sin,pi
import json

from visigoth.svg.svgstyled import svgstyled


# represent a section of text as an SVG tspan object
class tspan(svgstyled):

    def __init__(self,txt,tooltip="",font_height=None,text_attributes={}):
        svgstyled.__init__(self,"tspan",tooltip)
        self.setContent(txt)
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.url = None

    def setUrl(self,url):
        self.url = url

    def render(self,svgdoc,parent):
        dattrs = svgdoc.getDiagram().getDefaultTextAttributes()
        self.addAttrs(dattrs)

        if self.text_attributes:
            self.addAttrs(self.text_attributes)

        if self.font_height:
            self.addAttr("font-size",self.font_height)

        font_family = self.text_attributes.get("font-family",dattrs.get("font-family",""))
        font_weight = self.text_attributes.get("font-weight",dattrs.get("font-weight","normal"))
        font_style = self.text_attributes.get("font-style",dattrs.get("font-style","normal"))

        svgdoc.includeFont(font_family,font_weight,font_style)

        if self.url:
            doc = svgdoc.doc
            self.addAttr("text-decoration","underline")
            self.addAttr("stroke", "blue")
            p = doc.createElement("a")
            parent.appendChild(p)
            p.setAttribute("href",self.url)
            p.setAttribute("target","_new")
            parent = p

        return super(tspan, self).render(svgdoc, parent)
