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

from visigoth.svg.javascript_snippet import javascript_snippet
from visigoth.svg.svgdefinition import svgdefinition
from visigoth.svg.group import group
from visigoth.utils.js import Js
from visigoth.utils.fonts.fontmanager import FontManager
from visigoth.svg.filters import glow
from visigoth.svg.css_snippet import css_snippet

class svgdoc(object):

    # construct a document with an owning Diagram plus a given width and height
    def __init__(self,diagram,width,height,format,html_title=""):
        self.diagram = diagram
        self.definitions = [glow()]
        self.objects = []
        self.codez = []
        self.width = width
        self.height = height
        self.presentation_steps = []
        self.groups = []
        self.pop_groups = []
        self.style = ""
        self.code_cache = {}
        self.fonts = set()
        self.embed_fonts = False
        self.doc = None
        self.editable = False
        self.format = format
        self.html_title = html_title

    def setEditable(self,editable):
        self.editable = editable

    def getEditable(self):
        return self.editable

    def setEmbedFonts(self,embed):
        self.embed_fonts = embed

    def getDoc(self):
        return self.doc

    def getDiagram(self):
        return self.diagram

    def includeFont(self,family,weight,style):
        self.fonts.add((family,weight,style))

    def addStyle(self,style):
        self.definitions.append(style)

    def getCodeCache(self):
        return self.code_cache

    def getPopGroups(self):
        return self.pop_groups

    def setPopGroups(self,pop_groups):
        self.pop_groups = pop_groups
        
    def openGroup(self,group_id=None,popup=False):
        g = group()
        g.setId(group_id)
        if popup:
            self.pop_groups.append(g)
        else:
            self.add(g)
        self.groups.append(g)
        return g

    def closeGroup(self):
        if len(self.groups):
            closing_group = self.groups[-1]
            self.groups = self.groups[:-1]
            return closing_group
        else:
            return None

    # add an object to the document (obj inherits from svgstyled)
    def add(self,obj):
        if isinstance(obj,svgdefinition):
            self.definitions.append(obj)
        else:
            if len(self.groups):
                self.groups[-1].add(obj)
            else:
                self.objects.append(obj)
        return self

    def addCode(self,code):
        self.codez.append(code)

    def addPresentationStep(self,index,anchorName):
        self.presentation_steps.append({"index":index,"anchor":anchorName})

    def construct(self):

        self.doc = Document()

        self.root = self.doc.createElement("svg")
        self.root.setAttribute("xmlns","http://www.w3.org/2000/svg")
        self.root.setAttribute("xmlns:xlink","http://www.w3.org/1999/xlink")
        self.defs = self.doc.createElement("defs")
        self.root.appendChild(self.defs)
        if self.style:
            style = self.doc.createElement("style")
            styletext = self.doc.createTextNode(self.style)
            style.appendChild(styletext)
            self.root.appendChild(style)

        self.root.setAttribute("xmlns:svg","http://www.w3.org/2000/svg")
        self.root.setAttribute("xmlns","http://www.w3.org/2000/svg")
        self.root.setAttribute("width","%d"%(self.width))
        self.root.setAttribute("height", "%d" % (self.height))
        self.root.setAttribute("version", "1.1")
        self.root.setAttribute("onload","pubsubs_publish(\"\",\"load\");")

        title = self.diagram.getTitle()
        if title:
            t = self.doc.createElement("title")
            t.appendChild(self.doc.createTextNode(title))
            self.root.appendChild(t)

        description = self.diagram.getDescription()
        if description:
            t = self.doc.createElement("desc")
            t.appendChild(self.doc.createTextNode(description))
            self.root.appendChild(t)

        # add the definitions
        for o in self.definitions:
            o.render(self)

        # add the objects
        for o in self.objects:
            o.render(self,self.root)

        # add the popup objects
        for o in self.pop_groups:
            o.render(self,self.root)

        if self.codez:
            o = javascript_snippet("\n\n"+"\n\n".join(self.codez))
            o.render(self)

        if self.embed_fonts:
            for (name,weight,style) in self.fonts:
                if FontManager.containsFont(name,weight,style):
                    o = css_snippet(FontManager.getCssFontFace(name,weight,style))
                    o.render(self)
        else:
            font_names = set()
            for (name,_,_) in self.fonts:
                font_names.add(name)
            for name in font_names:
                o = css_snippet(FontManager.getCssFontImport(name))
                o.render(self)

        if self.format == "html":
            html = self.doc.createElement("html")
            head = self.doc.createElement("head")
            body = self.doc.createElement("body")
            html.appendChild(head)
            html.appendChild(body)

            if self.html_title:
                title = self.doc.createElement("title")
                title.appendChild(self.doc.createTextNode(self.html_title))
                head.appendChild(title)

            body.appendChild(self.root)

            self.doc.appendChild(html)
        else:
            self.doc.appendChild(self.root)
        return self.doc
        
    def render(self):
        doc = self.construct()
        return doc.toprettyxml(encoding="utf-8")

