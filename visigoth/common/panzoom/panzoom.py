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

from visigoth.svg import circle, rectangle, line, sector, triangle
from visigoth.common.text import Text
from visigoth.utils.js import Js
from visigoth.common import DiagramElement

import os
import math

class PanZoom(DiagramElement):
    """
    Create a pan/zoom control

    Keyword Arguments:
        radius(int): radius of control in pixels
        fill(str): the background colour for the button
        stroke(str): the stroke colour for the line around the button
        stroke_width(int): the stroke width for the line around the button

    Notes:
        When pressed the control will generate an event 
    """
    def __init__(self,zoom_to,initial_zoom=1,radius=30,fill="white",stroke="black",stroke_width=1):
        super(PanZoom,self).__init__()
        self.zoom_to = zoom_to
        self.radius = radius
        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.initial_zoom = initial_zoom
        
    def build(self,fmt):
        if fmt != "html":
            self.width = 0
            self.height = 0
        else:
            self.width = 2*self.radius
            self.height = 2*self.radius
    
    def draw(self,d,cx,cy):
        if d.getFormat() != "html":
            return
        c = circle(x=cx,y=cy,r=self.radius,fill=self.fill)
        c.addAttr("opacity",0.6)
        d.add(c)

        button_size = self.radius/2.2
        bx = cx - button_size/2
        by1 = cy - button_size
        by1 -= button_size*0.1
        
        by2 = cy
        by2 += button_size*0.1 
        r1 = rectangle(bx,by1,button_size,button_size,self.fill,rx=button_size/5,ry=button_size/5,stroke=self.stroke,stroke_width=self.stroke_width)
        r2 = rectangle(bx,by2,button_size,button_size,self.fill,rx=button_size/5,ry=button_size/5,stroke=self.stroke,stroke_width=self.stroke_width)

        l1a = line(bx+button_size*0.2,by1+button_size/2,bx+button_size*0.8,by1+button_size/2,self.stroke,self.stroke_width)
        l1b = line(bx+button_size/2,by1+button_size*0.2,bx+button_size/2,by1+button_size*0.8,self.stroke,self.stroke_width)

        l2 = line(bx+button_size*0.2,by2+button_size/2,bx+button_size*0.8,by2+button_size/2,self.stroke,self.stroke_width)
        
        plusg = d.openGroup()
        plusId = plusg.getId()
        d.add(r1).add(l1a).add(l1b)
        plusg.addAttr("tabindex","0")
        d.closeGroup()

        minusg = d.openGroup()
        minusId = minusg.getId()
        d.add(r2).add(l2)
        minusg.addAttr("tabindex","0")
        d.closeGroup()

        sr1 = self.radius*0.75
        sr2 = self.radius
        n = sector(cx,cy,sr1,sr2,math.pi*0.3,math.pi*0.7,fill=self.fill,stroke=self.stroke,stroke_width=self.stroke_width)
        e = sector(cx,cy,sr1,sr2,math.pi*0.8,math.pi*1.2,fill=self.fill,stroke=self.stroke,stroke_width=self.stroke_width)
        s = sector(cx,cy,sr1,sr2,math.pi*1.3,math.pi*1.7,fill=self.fill,stroke=self.stroke,stroke_width=self.stroke_width)
        w = sector(cx,cy,sr1,sr2,math.pi*1.8,math.pi*0.2,fill=self.fill,stroke=self.stroke,stroke_width=self.stroke_width)
        
        t_radius = self.radius/8
        sr = 0.87
        t_n = triangle(cx,cy-self.radius*sr,t_radius,math.pi,fill=self.stroke)
        t_e = triangle(cx+self.radius*sr,cy,t_radius,math.pi/2,fill=self.stroke)
        t_s = triangle(cx,cy+self.radius*sr,t_radius,0,fill=self.stroke)
        t_w = triangle(cx-self.radius*sr,cy,t_radius,math.pi*1.5,fill=self.stroke)
        
        ng = d.openGroup()
        nId = ng.getId()
        d.add(n).add(t_n).closeGroup()
        ng.addAttr("tabindex","0")

        eg = d.openGroup()
        eId = eg.getId()
        d.add(e).add(t_e).closeGroup()
        eg.addAttr("tabindex","0")

        sg = d.openGroup()
        sId = sg.getId()
        d.add(s).add(t_s).closeGroup()
        sg.addAttr("tabindex","0")

        wg = d.openGroup()
        wId = wg.getId()
        d.add(w).add(t_w).closeGroup()
        wg.addAttr("tabindex","0")

        sr1 = self.radius * 0.6
        sr2 = self.radius * 0.7

        zoom_level = 1
        zoom_levels = []
        while zoom_level <= self.zoom_to:
            zoom_levels.append(zoom_level)
            half_level = zoom_level * 1.5
            if half_level <= self.zoom_to:
                zoom_levels.append(half_level)
            zoom_level *= 2

        nr_segments = len(zoom_levels)
        segments = []
        angle = math.pi * 0.5
        awidth = math.pi / (nr_segments+0.5)
        astep = 2 * math.pi / nr_segments

        for i in range(len(zoom_levels)):
            if i == 0:
                sfill = self.stroke
            else:
                sfill = self.fill
            seg = sector(cx,cy,sr1,sr2,angle-awidth,angle+awidth,fill=sfill,stroke=self.stroke,stroke_width=self.stroke_width)
            segments.append(seg.getId())
            d.add(seg)
            angle += astep
        
        with open(os.path.join(os.path.split(__file__)[0],"panzoom.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = {
            "initial_zoom":self.initial_zoom,
            "zoom_levels":zoom_levels, "fill":self.fill, "stroke":self.stroke,
            "plus":plusId, "minus":minusId, "n":nId, "e":eId, "s":sId, "w":wId, 
            "zoom_segments":segments,
            "btn_n":n.getId(), "btn_e":e.getId(), "btn_s":s.getId(), "btn_w":w.getId(), 
            "btn_plus":r1.getId(), "btn_minus":r2.getId() }
        Js.registerJs(d,self,jscode,"panzoom",cx,cy,config)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height