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
        self.container = None
        self.form = None

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

    def setContainer(self,container):
        self.container = container

    def getContainer(self):
        return self.container

    def remove(self,element):
        raise Execption("Remove element not supported")

    def getId(self):
        return self.id

    def build(self):
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

    def search(self,element_id):
        if self.id == element_id:
            return self
        else:
            return None
