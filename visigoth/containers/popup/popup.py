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
from visigoth.common.image import Image
from visigoth.common.button import Button
from visigoth.svg import rectangle,text
from visigoth.utils.js import Js

import os

class Popup(DiagramElement):

    """
    Wrap an element within a closable popup box

    Arguments:
        element(DiagramElement): element to wrap
        title(str): title for the popup

    Keyword Arguments:
        stroke_width(int): width of the border in pixels
        stroke(str): colour of the border
        fill(str): fill colour for the box
        popup_group_id(str): (optional) id of an enclosing svg <g> element
        opacity(float): set the opacity of the popup, in range 0.0 (transparent) to 1.0 (opaque)
        corner_radius(float): radius of the popup corners in pixels
        font_height(int) : font size in pixels
        text_attributes(dict): a dict containing SVG name/value attributes
        opened(boolean): True iff the popup should be initially open
    """

    def __init__(self,element,title="",stroke_width=2,stroke="grey",fill="white",popup_group_id=None,opacity=1.0,corner_radius=4,font_height=18,text_attributes={},opened=False):
        DiagramElement.__init__(self)
        self.element = element
        self.element.setContainer(self)
        self.title = title
        self.stroke_width = stroke_width
        self.stroke = stroke
        self.height = 0
        self.width = 0
        self.fill = fill
        self.opened = opened
        self.popup_group_id = popup_group_id
        self.opacity = opacity
        self.font_height = font_height
        self.titlebar_height = self.font_height*2
        self.footer_height = self.titlebar_height
        self.text_attributes = text_attributes
        self.built = False
        self.close_button_stroke_width = self.titlebar_height / 10
        self.close_button_stroke = "red"
        self.corner_radius = corner_radius
        folder = os.path.split(__file__)[0]

        with open(os.path.join(folder,"close_ionicon.svg"),"rb") as iconfile:
            self.close_img = Image(mime_type="image/svg+xml",content_bytes=iconfile.read(),height=self.titlebar_height*0.5,width=self.titlebar_height*0.5,tooltip="Close")
            self.close_btn = Button(image=self.close_img,fill=self.fill,stroke=self.stroke, padding=2, r=self.corner_radius, click_value="close")

    def build(self):
        if not self.built:
            self.element.build()
            self.close_btn.build()
            self.width = self.stroke_width*2+self.element.getWidth()
            self.height = self.titlebar_height+self.stroke_width*2+self.element.getHeight()
        self.built = True

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def draw(self,doc,cx,cy):
        y = cy - self.height/2
        x = cx

        pg = doc.openGroup()
        pg.addAttr("opacity",self.opacity)
        if not self.opened:
            pg.addAttr("visibility","hidden")
        pgid = pg.getId()

        ex = cx - self.width/2 + self.stroke_width+self.element.getWidth()/2
        ey = cy - self.height/2 + self.titlebar_height+self.stroke_width+self.element.getHeight()/2

        border_height = self.element.getHeight()+self.stroke_width+self.titlebar_height+self.corner_radius
        border = rectangle(x-self.width/2,y,self.width,border_height,stroke_width=self.stroke_width,stroke=self.stroke,fill=self.fill,rx=self.corner_radius,ry=self.corner_radius)
        doc.add(border)

        titletext = text(x-self.width/2+self.titlebar_height/4,y+self.titlebar_height/2,self.title,font_height=self.font_height,text_attributes=self.text_attributes)
        titletext.addAttr("text-anchor","start")
        titletext.setVerticalCenter()
        doc.add(titletext)

        doc.openGroup()
        closebutton_ox = x+self.width/2-self.close_btn.getWidth()
        closebutton_oy = y+self.titlebar_height/2
        self.close_btn.draw(doc,closebutton_ox,closebutton_oy)
        doc.closeGroup()

        self.element.draw(doc,ex,ey)

        pgid = doc.closeGroup().getId()
        if not self.popup_group_id:
            self.popup_group_id = pgid

        with open(os.path.join(os.path.split(__file__)[0],"popup.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = { "pgid":pgid }
        
        Js.registerJs(doc,self,jscode,"popup",cx,cy,config)

        doc.getDiagram().connect(self.close_btn,"click",self,"click")
        return pg

    def search(self,element_id):
        e = self.element.search(element_id)
        if e:
            return e
        
        return super(Popup,self).search(element_id)

