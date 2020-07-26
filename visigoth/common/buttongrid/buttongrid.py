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

from visigoth.containers import Grid
from visigoth.utils.js import Js
from visigoth.common import DiagramElement

import os

class ButtonGrid(DiagramElement):
    """
    Create a "grid" holding multiple buttons, parameters define defaults for buttons

     Keyword Arguments:
        stroke_width(int): width of the grid lines in pixels
        stroke(str): colour of the grid lines
        padding(int): width of the cell padding in pixels
        fill(str): fill colour for the cells

    Notes:
        When one of the buttons is pressed the buttongrid will generate an event with the value set to
        the click_value associated with the button on channel "click"
    """
    def __init__(self,stroke=None,stroke_width=0,padding=10,fill=None):
        super(ButtonGrid,self).__init__()
        self.grid = Grid(stroke=stroke,stroke_width=stroke_width,padding=padding,fill=fill)
        self.buttons = []
        self.width = 0
        self.height = 0

    def addButton(self,row,column,button,initially_selected=False):
        self.grid.add(row,column,button)
        self.buttons.append(button)
        if initially_selected:
            button.setInitiallySelected()

    def build(self,fmt):
        if fmt != "html":
            return
        self.grid.build(fmt)
        self.height = self.grid.getHeight()
        self.width = self.grid.getWidth()

    def draw(self,d,cx,cy):
        if d.getFormat() != "html":
            return
        self.grid.draw(d,cx,cy)
        with open(os.path.join(os.path.split(__file__)[0],"buttongrid.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = { "button_channels":["ch"+button.getId() for button in self.buttons] }
        Js.registerJs(d,self,jscode,"buttongrid",cx,cy,config)

        for button in self.buttons:
            btn_channel = "ch"+button.getId()
            d.getDiagram().connect(button,"click",self,"click")
            d.getDiagram().connect(button,btn_channel,self,btn_channel)
            d.getDiagram().connect(self,btn_channel,button,btn_channel)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height