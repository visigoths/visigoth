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

from visigoth.common.diagram_element import DiagramElement

class Sequence(DiagramElement):
    """
    Construct a container holding multiple elements in a sequence layout

    Keyword Arguments:
        spacing(int): spacing between elements in pixels
        orientation(str): vertical|horizontal whether to layout the sequence top-to-bottom or left-to-right

    The way you might use me is:

    >>> d = Diagram()
    >>> s = Sequence()
    >>> s.add(Text("Here is some text"))
    >>> s.add(Text("Here is some more text"))
    >>> d.add(s)
    """

    def __init__(self,spacing=20,orientation="vertical"):
        DiagramElement.__init__(self)
        self.elements = []
        self.spacing = spacing
        self.layout = orientation

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def build(self):
        for idx in range(len(self.elements)):
            element = self.elements[idx]
            element.build()

        total_spacing = 0
        if len(self.elements):
            total_spacing = self.spacing*(len(self.elements)-1)

        if self.layout == "vertical":
            self.width = max([element.getWidth() for element in self.elements])
            self.height = total_spacing+sum([element.getHeight() for element in self.elements])
        else:
            self.width = total_spacing+sum([element.getWidth() for element in self.elements])
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
        off_y = cy-self.height/2
        off_x = cx-self.width/2

        if self.layout == "vertical":
            for e in self.elements:
                ecx = cx
                if e.getLeftJustified():
                    ecx = off_x + e.getWidth()/2
                elif e.getRightJustified():
                    ecx = cx + self.width/2 - e.getWidth()/2
                e.draw(doc, ecx, off_y+e.getHeight()/2)
                off_y += self.spacing + e.getHeight()
        else:
            for e in self.elements:
                e.draw(doc, off_x+e.getWidth()/2, cy)
                off_x += self.spacing + e.getWidth()

    def search(self,element_id):
        for e in self.elements:
            se = e.search(element_id)
            if se:
                return se
        
        return super(Sequence,self).search(element_id)