# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

from visigoth.containers import Grid, Box
from visigoth.common import DiagramElement, Text
from visigoth.utils.colour import DiscreteColourManager, ContinuousColourManager

from visigoth.utils.data.dataset import Dataset

import os

class Table(DiagramElement):
    """
    Create a "grid" holding multiple text elements

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)

     Keyword Arguments:
        headings: list of [(column,heading)] pairs
        colour (str or int): Identify the column to specify the line to which each row belongs
        max_column_width: maximum width of a column in pixels
        stroke_width(int): width of the grid lines in pixels
        stroke(str): colour of the grid lines
        colour_manager(object) : a ContinuousColourManager or DiscreteColourManager instance to control row colour
        padding(int): width of the cell padding in pixels
        fill(str): fill colour for the cells
        font_height(int): the font size for the legend (optional, defaults to 24)
        text_attributes(dict): a dict containing SVG name/value pairs to apply to table body text
        header_text_attributes(dict): a dict containing SVG name/value pairs to apply to table header text
    """
    def __init__(self,data,headings=[],colour=None,max_column_width=None,stroke="grey",colour_manager=None,stroke_width=2,padding=10,fill=None,font_height=24,text_attributes={},header_text_attributes={"font-weight":"bold"}):
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
        self.colour_manager = colour_manager
        if not self.colour_manager and self.colour != None:
            if self.dataset.isDiscrete(self.colour):
                self.colour_manager = DiscreteColourManager()
            else:
                self.colour_manager = ContinuousColourManager()

        self.max_column_width = max_column_width
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.header_text_attributes = header_text_attributes
        if self.colour != None:
            for val in self.dataset.query([self.colour],unique=True,flatten=True):
                self.getPalette().allocateColour(val)

    def getPalette(self):
        return self.colour_manager

    def build(self,fmt):
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


        self.grid.build(fmt)
        self.height = self.grid.getHeight()
        self.width = self.grid.getWidth()

    def draw(self,d,cx,cy):
        self.grid.draw(d,cx,cy)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height