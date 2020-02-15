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

class Space(DiagramElement):
    """
    Define an area of whitespace in the diagram

    Arguments:
        height(int): height of the whitespace in pixels

    Keyword Arguments:
        width(int): width of the whitespace in pixels
    """

    def __init__(self,height,width=0):

        DiagramElement.__init__(self)
        self.height = height
        self.width = width

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width
