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

# base class for SVG objects, holding style information and handing rendering
class svgstyled(object):

    idcounter = 0

    def __init__(self,tag,tooltip=""):
        self.tag = tag
        self.style = {}
        self.attrs = {}
        self.tooltip = tooltip
        self.content = ''
        self.handlers = {}
        self.children = []
        self.animations = []
        self.id = ""


    def setId(self,eid=None):
        if eid:
            self.id = eid
        else:
            svgstyled.idcounter += 1
            self.id = "s"+str(svgstyled.idcounter)
        return self.id

    def getId(self):
        if self.id == "":
            return self.setId()
        else:
            return self.id

    def addChild(self,ele):
        self.children.append(ele)

    # add an SVG attribute
    def addAttr(self,name,value):
        self.attrs[name] = value
        return self

    # add an animation
    def addAnimation(self,propertyName,fromValue,toValue,durationSecs):
        self.animations.append((propertyName,fromValue,toValue,durationSecs))

    def getAttr(self,name):
        return self.attrs[name]

    # add multiple SVG attributes
    def addAttrs(self,attrs):
        if attrs:
            for k in attrs:
                self.addAttr(k,attrs[k])
        return self

    # add a handler
    def addHandler(self,evt,fname):
        self.handlers[evt] = fname

    # get handler if defined
    def getHandler(self,evt):
        if evt in self.handlers:
            return self.handlers[evt]
        return None

    # set the XML content of the element
    def setContent(self,content):
        self.content = content
        return self

    # construct the style attribute
    def getStyleAttr(self):
        keys = self.style.keys()
        s = ''
        if len(keys):
            for k in keys:
                s += k + ":" + str(self.style[k])+";"
        return s

    # set the tooltp
    def setTooltip(self,tooltip):
        self.tooltip = tooltip

    def render(self,svgdoc,parent):
        doc = svgdoc.doc
        if self.tooltip:
            g = doc.createElement("g")
            title = doc.createElement("title")
            title.appendChild(doc.createTextNode(self.tooltip))
            g.appendChild(title)
            parent.appendChild(g)
            parent = g

        e = doc.createElement(self.tag)
        for name in self.attrs:
            e.setAttribute(name,str(self.attrs[name]))

        for evt in self.handlers:
            fname = self.handlers[evt]
            e.setAttribute("on"+evt,"return "+fname+"(evt);")

        style = self.getStyleAttr()
        if style:
            e.setAttribute("style",style)

        parent.appendChild(e)

        if self.content != '':
            e.appendChild(doc.createTextNode(self.content))

        for child in self.children:
            e.appendChild(child)

        for animation in self.animations:
            (propertyName,fromValue,toValue,durationSecs) = animation
            a = doc.createElement("animate")
            a.setAttribute("attributeType","XML");
            a.setAttribute("attributeName",propertyName)
            a.setAttribute("from",str(fromValue))
            a.setAttribute("to",str(toValue))
            a.setAttribute("dur",str(durationSecs)+"s")
            a.setAttribute("repeatCount","indefinite")
            e.appendChild(a)

        if self.id:
            e.setAttribute("id",self.id)
        return e
