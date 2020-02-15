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
import json

from visigoth.svg.svgdefinition import svgdefinition

class clip_path(svgdefinition):

    counter = 0

    def __init__(self):
        svgdefinition.__init__(self,"cp_"+str(clip_path.counter))
        clip_path.counter += 1
        self.regions = []

    def addRegion(self,ele):
        self.regions.append(ele)

    def render(self,svgdoc):
        doc = svgdoc.doc
        cp = doc.createElement("clipPath")
        cp.setAttribute("id",self.getId())
        for region in self.regions:
            region.render(svgdoc,cp)
        svgdoc.defs.appendChild(cp)
        return cp