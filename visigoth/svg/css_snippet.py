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

class css_snippet(svgdefinition):

    counter = 0

    def __init__(self,css):
        svgdefinition.__init__(self,"style_"+str(css_snippet.counter))
        css_snippet.counter += 1
        self.css = css

    def render(self,svgdoc):
        doc = svgdoc.doc
        s = doc.createElement("style")
        s.setAttribute("id", self.getId())
        s.setAttribute("type","text/css")
        tn = doc.createCDATASection("\n"+self.css+"\n")
        s.appendChild(tn)
        svgdoc.defs.appendChild(s)
        return s
