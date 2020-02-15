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

from visigoth.svg.svgstyled import svgstyled

class group(svgstyled):

    def __init__(self):
        super(group, self).__init__("g")
        self.child_elements = []

    def add(self,child):
        self.child_elements.append(child)

    def render(self,svgdoc,parent):
        g = super(group,self).render(svgdoc,parent)
        for t in self.child_elements:
            t.render(svgdoc,g)
        parent.appendChild(g)
        return g