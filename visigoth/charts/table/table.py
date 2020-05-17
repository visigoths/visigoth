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

from visigoth.containers import Grid, Box
from visigoth.common import DiagramElement, Text
from visigoth.utils.colour import DiscretePalette, ContinuousPalette

from visigoth.utils.data.dataset import Dataset

import os

class Table(DiagramElement):
    """
    Create a "grid" holding multiple buttons, parameters define defaults for buttons

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)

     Keyword Arguments:
        headings: list of [(column,heading)] pairs
        colour (str or int): Identify the column to specify the line to which each row belongs
        max_column_width: maximum width of a column in pixels
        stroke_width(int): width of the grid lines in pixels
        stroke(str): colour of the grid lines
        palette(object) : a ContinuousPalette or DiscretePalette instance to control row colour
        padding(int): width of the cell padding in pixels
        fill(str): fill colour for the cells
        font_height(int): the font size for the legend (optional, defaults to 24)
        text_attributes(dict): a dict containing SVG name/value pairs to apply to table body text
        header_text_attributes(dict): a dict containing SVG name/value pairs to apply to table header text
    """
    def __init__(self,data,headings=[],colour=None,max_column_width=None,stroke="grey",palette=None,stroke_width=2,padding=10,fill=None,font_height=24,text_attributes={},header_text_attributes={"font-weight":"bold"}):
        super(Table,self).__init__()
        self.grid = Grid(stroke=stroke,stroke_width=stroke_width,padding=padding,fill=fill)
        self.dataset = Dataset(data)
        headings = headings if headings else self.dataset.getColumns()
        self.headings = []
        for heading in headings:
            if isinstance(heading,str):
                heading = [heading]
            col = heading[0]
            name = heading[1] if len(heading)>1 else col
            formatter = heading[2] if len(heading)>2 else lambda x:str(x)
            self.headings.append((col,name,formatter))
        self.colour = colour
        self.palette = palette
        if not self.palette and self.colour != None:
            if self.dataset.isDiscrete(self.colour):
                self.palette = DiscretePalette()
            else:
                self.palette = ContinuousPalette()

        self.max_column_width = max_column_width
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.header_text_attributes = header_text_attributes
        if self.colour != None:
            for val in self.dataset.query([self.colour],unique=True,flatten=True):
                self.getPalette().getColour(val)

    def getPalette(self):
        return self.palette

    def build(self):
        rowdata = self.dataset.query([col for (col,_,_) in self.headings])
        for col in range(len(self.headings)):
            (_, heading, _) = self.headings[col]
            t = Text(str(heading), font_height=self.font_height, text_attributes=self.header_text_attributes,max_width=self.max_column_width)
            if self.getLeftJustified():
                t.setLeftJustified()
            elif self.getRightJustified():
                t.setRightJustified()
            self.grid.add(0, col,t)

        for row in range(len(rowdata)):
            values = rowdata[row]
            for col in range(len(self.headings)):
                (_, heading, fmtfn) = self.headings[col]
                t = Text(fmtfn(values[col]), font_height=self.font_height, text_attributes=self.text_attributes,max_width=self.max_column_width)
                if self.getLeftJustified():
                    t.setLeftJustified()
                elif self.getRightJustified():
                    t.setRightJustified()
                ele = t
                if col == self.colour:
                    colour = self.getPalette().getColour(values[col])
                    ele = Box(t,stroke_width=0,fill=colour)
                self.grid.add(row+1,col,ele)


        self.grid.build()
        self.height = self.grid.getHeight()
        self.width = self.grid.getWidth()

    def draw(self,d,cx,cy):
        self.grid.draw(d,cx,cy)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height