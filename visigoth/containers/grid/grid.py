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
from visigoth.svg import line, rectangle

import base64

class Grid(DiagramElement):
    """
    A grid layout

    Keyword Arguments:
        stroke_width(int): width of the grid lines in pixels
        stroke(str): colour of the grid lines
        padding(int): width of the cell padding in pixels
        fill(str): fill colour for the cells

    Note: use the add method to add elements to the grid
    """

    def __init__(self,stroke=None,stroke_width=0,padding=10,fill=None):
        DiagramElement.__init__(self)
        self.height = 0
        self.width = 0
        self.cells = {}
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.padding = padding
        self.fill = fill
        self.col_widths = {}
        self.row_heights = {}
        self.max_row = 0
        self.max_col = 0


    def add(self,row,col,element):
        """
        Add an element into the grid

        Arguments:
            row(int) : the number of the row (numbering starts at 0, top to bottom)
            col(int) : the number of the column (numbering starts at 0, left to right)
            element(DiagramElement) : the element to add
        """
        self.cells[(row,col)] = element
        element.setContainer(self)

    def getCellWidth(self,cell):
        return cell.getWidth()+2*self.padding+2*self.stroke_width/2

    def getCellHeight(self,cell):
        return cell.getHeight()+2*self.padding+2*self.stroke_width/2

    def build(self):
        for (row,col) in self.cells:
            cell = self.cells[(row,col)]
            cell.build()
            if col not in self.col_widths:
                self.col_widths[col] = 0
            self.col_widths[col] = max(self.col_widths[col],self.getCellWidth(cell))
            if row not in self.row_heights:
                self.row_heights[row] = 0
            self.row_heights[row] = max(self.row_heights[row],self.getCellHeight(cell))

        self.max_row = max([row for (row,col) in self.cells])
        self.max_col = max([col for (row,col) in self.cells])
        
        self.width = sum([w for w in self.col_widths.values()])
        self.height = sum([h for h in self.row_heights.values()])

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def draw(self,d,cx,cy):
        oy = cy - self.height/2
        ox = cx - self.width/2

        ry = oy
        for row in range(self.max_row+1):
            rx = ox
            if row in self.row_heights:
                for col in range(self.max_col+1):
                    if col in self.col_widths:
                        cw = self.col_widths[col]
                        rh = self.row_heights[row]
                        if (row,col) in self.cells:
                            ele = self.cells[(row,col)]

                            if ele.getLeftJustified():
                                ecx = rx + self.getCellWidth(ele)/2
                            elif ele.getRightJustified():
                                ecx = rx + cw - self.getCellWidth(ele)/2
                            else:
                                ecx = rx + cw/2
                            if self.fill:
                                r = rectangle(rx,ry,self.getCellWidth(ele),self.getCellHeight(ele),fill=self.fill)
                                d.add(r)
                            ele.draw(d,ecx,ry+rh/2)
                        rx += cw
                ry += self.row_heights[row]

        if self.stroke and self.stroke_width:
            self.drawGrid(d,ox,oy)

    def drawGrid(self,d,ox,oy):
        ry = oy
        for row in range(self.max_row+1):
            if row in self.row_heights:
                gridline = line(ox,ry,ox+self.width,ry,self.stroke,self.stroke_width)
                d.add(gridline)
                ry += self.row_heights.get(row)
        gridline = line(ox,ry,ox+self.width,ry,self.stroke,self.stroke_width)
        d.add(gridline)

        rx = ox
        for col in range(self.max_col+1):
            if col in self.col_widths:
                gridline = line(rx,oy,rx,oy+self.height,self.stroke,self.stroke_width)
                d.add(gridline)
                rx += self.col_widths.get(col)
        gridline = line(rx,oy,rx,oy+self.height,self.stroke,self.stroke_width)
        d.add(gridline)

    def search(self,element_id):
        for key in self.cells:
            e = self.cells[key].search(element_id)
            if e:
                return e
        
        return super(Grid,self).search(element_id)



