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

import os
import os.path

from visigoth.common.diagram_element import DiagramElement
from visigoth.utils.js import Js

class Alternative(DiagramElement):
    """
    Construct a container holding multiple elements.  Only one element is displayed at any one time.
    """

    def __init__(self):
        DiagramElement.__init__(self)
        self.elements = []

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def build(self):
        for element in self.elements:
            element.build()

        self.width = max([element.getWidth() for element in self.elements])
        self.height = max([element.getHeight() for element in self.elements])

    def add(self,element):
        """
        Add an element to the sequence to appear after previously added elements

        Arguments:
            element(DiagramElement): the element to append to the sequence
        """
        self.elements.append(element)
        element.setContainer(self)
        return self

    def remove(self,element):
        self.elements.remove(element)

    def draw(self,doc,cx,cy):
        group_ids = []
        for e in self.elements:
            doc.openGroup(group_id=e.getId())
            e.draw(doc, cx, cy)
            group_ids.append(e.getId())
            doc.closeGroup()

        with open(os.path.join(os.path.split(__file__)[0],"alternative.js"),"r") as jsfile:
            jscode = jsfile.read()

        config = { "group_ids": group_ids }

        Js.registerJs(doc,self,jscode,"alternative",cx,cy,config)

