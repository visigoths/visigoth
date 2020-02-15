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

from xml.dom.minidom import *
from math import cos,sin,pi
import json

from visigoth.utils.fonts.fontmanager import FontManager
from visigoth.svg import rectangle,svgstyled


# represent a section of text as an SVG object
class text(svgstyled):

    def __init__(self,x,y,txt,tooltip="",font_height=None,text_attributes={},fill=None):
        svgstyled.__init__(self,"text",tooltip)
        self.x = x
        self.y = y
        self.txt = txt
        self.addAttr("x",x).addAttr("y",y).setContent(txt)
        self.url = ""
        self.addAttr("text-anchor", "middle")
        self.rotation = None
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.fill = fill
        self.vertical_center = False
        self.horizontal_center = True
        self.label_margin = 5

    def setUrl(self,url):
        self.url = url
        self.addAttr("text-decoration","underline")
        self.addAttr("stroke", "blue")
        return self

    def setRotation(self,radians):
        self.rotation = 360*radians/(2*pi)
        self.addAttr("transform","rotate(%f,%f,%f)"%(self.rotation,self.x,self.y))
        return self

    def setVerticalCenter(self,center=True):
        self.vertical_center = center
        if center:
            self.addAttr("dominant-baseline","middle")
        else:
            self.addAttr("dominant-baseline","top")
        return self

    def setHorizontalCenter(self,center=True):
        self.horizontal_center = center
        if center:
            self.addAttr("text-anchor","middle")
        else:
            self.addAttr("text-anchor","start")
        return self

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
            p = doc.createElement("a")
            parent.appendChild(p)

            p.setAttribute("href",self.url)
            p.setAttribute("target","_new")
            parent = p


        if self.fill:            
            l = FontManager.getTextLength(self.text_attributes,self.txt,self.font_height)
            rx = self.x - self.label_margin
            ry = self.y - self.font_height - self.label_margin
            if self.vertical_center:
                ry = self.y - self.font_height/2 - 5
            if self.horizontal_center:
                rx = self.x - l/2 - self.label_margin
            r = rectangle(rx,ry,l+2*self.label_margin,self.font_height+2*self.label_margin,fill=self.fill)
            
            if self.rotation != None:
                r.addAttr("transform","rotate(%f,%f,%f)"%(self.rotation,self.x,self.y))

            r.render(svgdoc,parent)

        return super(text, self).render(svgdoc, parent)
        
    