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

    def addButton(self,row,column,button,initially_selected=False):
        self.grid.add(row,column,button)
        self.buttons.append(button)
        if initially_selected:
            button.setInitiallySelected()

    def build(self):
        self.grid.build()
        self.height = self.grid.getHeight()
        self.width = self.grid.getWidth()

    def draw(self,d,cx,cy):
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