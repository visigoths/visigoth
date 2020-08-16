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
from math import cos,sin,pi
import json

from visigoth.svg.svgdefinition import svgdefinition
from visigoth.svg.group import group
from visigoth.utils.js import Js
from visigoth.utils.fonts.fontmanager import FontManager
from visigoth.svg.filters import glow
from visigoth.svg.css_snippet import css_snippet

from uuid import uuid4

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
        self.meta_version = ""
        self.meta_home_url = ""
        self.meta_repo_url = ""
        self.html_title = html_title
        self.markers = {}

    def getMarker(self,txt):
        uuid_s = str(uuid4())
        self.markers[uuid_s] = txt
        return uuid_s

    def getFormat(self):
        return self.format

    def setMetadata(self,version,home_url,repo_url):
        self.meta_version = version
        self.meta_home_url = home_url
        self.meta_repo_url = repo_url

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
        # self.root.setAttribute("onload","pubsubs_publish(\"\",\"load\");")

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

        metadesc = self.doc.createElement("desc")
        metadesc.appendChild(self.doc.createTextNode("Generated by visigoth v%s (home page: %s) (source code: %s)"
                                              %(self.meta_version,self.meta_home_url,self.meta_repo_url)))
        self.root.appendChild(metadesc)

        # add the definitions
        for o in self.definitions:
            o.render(self)

        # add the objects
        for o in self.objects:
            o.render(self,self.root)

        # add the popup objects
        for o in self.pop_groups:
            o.render(self,self.root)

        if self.embed_fonts:
            for font in self.fonts:
                (fname, weight, style) = font
                if FontManager.containsFont(fname,weight,style):
                    o = css_snippet(FontManager.getCssFontFace(fname,weight,style))
                    o.render(self)
        else:
            font_names = set()
            for font in self.fonts:
                (fname, _, _) = font
                font_names.add(fname)
            for name in font_names:
                o = css_snippet(FontManager.getCssFontImport(name))
                o.render(self)

        if self.format == "html":
            html = self.doc.createElement("html")
            head = self.doc.createElement("head")
            meta1 = self.doc.createElement("meta")
            meta1.setAttribute("charset", "UTF-8")
            head.appendChild(meta1)

            if self.codez:
                script = self.doc.createElement("script")
                script.setAttribute("type", "text/ecmascript")
                code = "function boot() {"+"\n\n".join(self.codez) + "\n\n};\n"
                marker = self.getMarker(code)
                script.appendChild(self.doc.createTextNode(marker))
                head.appendChild(script)

            body = self.doc.createElement("body")
            body.setAttribute("onload","boot()")
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
        xml = doc.toprettyxml(encoding="utf-8").decode("utf-8")
        for marker_uuid in self.markers:
            xml = xml.replace(marker_uuid,self.markers[marker_uuid])
        return xml

