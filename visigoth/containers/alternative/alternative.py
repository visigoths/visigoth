# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

    def build(self,fmt):
        if fmt == "html":
            for element in self.elements:
                element.build(fmt)

            self.width = max([element.getWidth() for element in self.elements])
            self.height = max([element.getHeight() for element in self.elements])
        else:
            self.elements[0].build(fmt)
            self.width = self.elements[0].width
            self.height = self.elements[0].height

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
        if doc.getFormat() == "html":
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
        else:
            self.elements[0].draw(doc,cx,cy)
