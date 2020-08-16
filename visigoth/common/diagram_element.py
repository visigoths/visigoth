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

from visigoth.svg import clip_path, rectangle

class DiagramElement(object):

    counter = 0

    @staticmethod
    def getNextId():
        DiagramElement.counter += 1
        return "diagelem"+str(DiagramElement.counter)

    """
    Superclass of all elements participating in a visigoth diagram

    element types may sub-class this or simply implement the build, getHeight, getWidth and draw methods
    """

    def __init__(self):
        self.id = DiagramElement.getNextId()
        self.ljustify = False
        self.rjustify = False
        self.editable = False

    def getLeftJustified(self):
        return self.ljustify

    def getRightJustified(self):
        return self.rjustify

    def setLeftJustified(self):
        self.ljustify = True
        self.rjustify = False
        return self

    def setRightJustified(self):
        self.rjustify = True
        self.ljustify = False
        return self

    def setEditable(self,isEditable=True):
        self.editable = isEditable

    def getEditable(self):
        return self.editable

    def getId(self):
        return self.id

    def build(self,fmt):
        """
        perform any computation required to prepare for drawing, and finalize the element height and width
        """
        pass

    def getHeight(self):
        """
        get the height of this element, in pixels

        the build method will be invoked before this method is called
        """
        return 0

    def getWidth(self):
        """
        get the width of this element, in pixels

        the build method will be invoked before this method is called
        """
        return 0

    def draw(self, d, cx, cy):
        """
        draw the element into the diagram at the specified coordinates

        the build method will be invoked before this method is called

        :param diagram: a visigoth.svg.svgdoc object
        :param cx: x-coordinate of the center of the element
        :param cy: y-coordinate of the center of the element

        """
        pass

    def openClip(self, doc, cx, cy, w=None, h=None):
        if not w:
            w = self.getWidth()
        if not h:
            h = self.getHeight()

        ox = cx - w/2
        oy = cy - h/2

        cp = clip_path()
        cp.addRegion(rectangle(ox,oy,w,h))
        doc.add(cp)

        g = doc.openGroup()
        g.addAttr("clip-path","url(#%s)"%(cp.getId()))

    def closeClip(self, doc):
        doc.closeGroup()

    def handleConnectTo(self,channel_out,dest_element):
        pass

    def handleConnectFrom(self,channel_in,source_element):
        pass
