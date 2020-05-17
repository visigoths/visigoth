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

from visigoth.svg import rectangle
from visigoth.common.text import Text
from visigoth.utils.js import Js
from visigoth.common import DiagramElement

import os

class Button(DiagramElement):
    """
    Create a button

    Keyword Arguments:
        text(str) : the text to display in the button
        image(visigoth.common.Image) : an image element to display in the button
        padding(int) : define padding around button content in pixels
        font_height(int) : font size in pixeks
        text_attributes(dict)x: a dict containing SVG name/value attributes
        url(str): url to link to from the text
        fill(str): the background colour for the button
        push_fill(str): the background colour for the button when pushed
        stroke(str): the stroke colour for the line around the button
        stroke_width(int): the stroke width for the line around the button
        r(int): the button corner radius in pixels
        click_value(str): the event value emitted when the button is clicked

    Notes:
        When pressed the button will generate an event with the value of the click_value parameter on channel "click"
    """
    def __init__(self,text=None,image=None,padding=2,font_height=24,text_attributes={},url=None,fill="white",push_fill="red",stroke="black",stroke_width=1,r=5,click_value="click"):
        super(Button,self).__init__()
        self.text = None
        self.image = None
        if not text and not image:
            text = "?"

        if text:
            self.text = Text(text,font_height=font_height,text_attributes=text_attributes,url=url)
        if image:
            self.image = image

        self.fill = fill
        self.push_fill = push_fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.r = r
        self.padding = padding
        self.click_value = click_value
        self.initially_selected = False

    def setInitiallySelected(self):
        self.initially_selected = True

    def build(self):
        if self.text:
            self.text.build()
        if self.image:
            self.image.build()
        self.width = self.padding
        self.height = 0
        if self.text:
            self.width += self.text.getWidth() + self.padding
        if self.image:
            self.width += self.image.getWidth() + self.padding
        if self.text:
            self.height += self.text.getHeight()
        if self.image and self.image.getHeight() > self.height:
            self.height = self.image.getHeight()
        self.height += 2*self.padding

    def draw(self,d,cx,cy):
        button_width = self.getWidth()
        button_height = self.getHeight()
        oy = cy - button_height/2
        ox = cx - button_width/2
        g = d.openGroup(self.getId())
        r = rectangle(ox,oy,button_width,button_height,self.fill,self.stroke,self.stroke_width,self.r,self.r)
        r.addAttr("tabindex","0")
        rid = r.getId()
        d.add(r)
        if self.image and self.text:
            tx = ox + self.padding + self.text.getWidth()/2
            self.text.draw(d,tx,cy)
            ix = ox + 2*self.padding + self.text.getWidth() + self.image.getWidth()/2
            self.image.draw(d,ix,cy)
        else:
            if self.text:
                self.text.draw(d,cx,cy)
            if self.image:
                self.image.draw(d,cx,cy)
        d.closeGroup()
        with open(os.path.join(os.path.split(__file__)[0],"button.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = { "initially_selected":self.initially_selected, "rectangle":rid, "fill":self.fill, "push_fill":self.push_fill, "click_value":self.click_value }
        Js.registerJs(d,self,jscode,"button",cx,cy,config)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height