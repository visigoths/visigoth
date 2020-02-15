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

from visigoth.svg.svgdefinition import svgdefinition

class javascript_snippet(svgdefinition):

    counter = 0

    def __init__(self,code,strip_comments=True):
        svgdefinition.__init__(self,"script_"+str(javascript_snippet.counter))
        javascript_snippet.counter += 1
        if strip_comments:
            code = "\n".join(filter(lambda line: line.find("//") != 0,code.split("\n")))
        self.code = code

    def getCode(self):
        return self.code

    def render(self,svgdoc):
        doc = svgdoc.doc
        s = doc.createElement("script")
        s.setAttribute("id", self.getId())
        s.setAttribute("type","text/ecmascript")
        tn = doc.createCDATASection("\n"+self.code+"\n")
        s.appendChild(tn)
        svgdoc.root.appendChild(s)
        return s
