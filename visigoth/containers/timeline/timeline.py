# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

import time
import math

from visigoth.common import DiagramElement
from visigoth.utils.fonts import FontManager
from visigoth.svg import text, line, circle, sector, cubic_bezier

class TimeLine(DiagramElement):

    def __init__(self, orientation="vertical", stroke="grey", stroke_width=10, font_height=24, text_attributes={}, branch_length=100, spacing=20):
        """
        Create a TimeLine, on to which labelled elements can be placed at specific dates/times

        :param orientation: the orientation, either "horizontal" or "vertical"
        :param stroke: the timeline colour
        :param stroke_width: the width of the timeline
        :param font_height: the font height for labels
        :param text_attributes: text attributes for labels
        :param branch_length: the offset from the line at which elements are aligned, in pixels
        :param spacing: space (in pixels) to leave between elements
        """

        DiagramElement.__init__(self)
        self.text_attributes = text_attributes
        self.elements = []
        self.timeline_width = stroke_width
        self.horizontal = True if orientation == "horizontal" else False
        self.branch_length = branch_length
        self.spacing = spacing
        self.colour = stroke
        self.width = 0
        self.height = 0
        self.left = False
        self.text_font_height = font_height
        self.pps = 0
        self.labelwidth = 0
        self.label_space = 20
        self.timeline_offset = 0

    def getUnixTime(self,dt):
        return time.mktime(dt.timetuple())

    def add(self,dt,element,label=None,offset=100):
        """
        Add an element to the timeline

        Arguments:
            dt(datetime.Datetime) : the date and time on the timeline
            element(DiagramElement) : the element to add

        Keyword Arguments:
            label(str) : the label to display on the timeline, in place of the date
        """
        self.elements.append((dt,element,label,offset))

    def build(self,fmt):
        if len(self.elements) == 0:
            return

        lstart = 0
        lend = 0
        length = 0
        start_dt = None
        end_dt = None
        first_e = None

        max_element_depth = 0
        max_label_depth = 0

        for index in range(len(self.elements)):
            (dt,e,label,offset) = self.elements[index]

            element_w = 0
            element_h = 0
            if e:
                e.build(fmt)
                element_w = e.getWidth()
                element_h = e.getHeight()
                if not first_e:
                    first_e = e

            if not self.horizontal:
                tw = 0
                if label:
                    tw = FontManager.getTextLength(self.text_attributes, label, self.text_font_height)
                l = element_h
                max_element_depth = max(max_element_depth,element_w)
                max_label_depth = max(tw,max_label_depth)
            else:
                th = 0
                if label:
                    th = self.text_font_height
                l = element_w
                max_element_depth = max(max_element_depth, element_h)
                max_label_depth = max(th, max_label_depth)

            if dt != None and start_dt == None:
                lstart = length + l/2
                start_dt = dt

            if e and e != first_e:
                length += self.spacing

            if dt != None:
                lend = length + l/2
                end_dt = dt

            length += l

        self.start_pos = self.getUnixTime(start_dt)
        self.end_pos = self.getUnixTime(end_dt)

        self.timeline_offset = self.label_space + max_label_depth
        depth = self.timeline_offset + self.timeline_width + self.branch_length + max_element_depth

        if self.horizontal:
            self.width = length
            self.height = depth
        else:
            self.width = depth
            self.height = length

        self.pps = (lend - lstart) / (self.end_pos - self.start_pos)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def draw(self,diagram,cx,cy):

        oy = cy - self.height/2
        ox = cx - self.width/2

        if self.horizontal:
            oy = oy + self.height-self.timeline_offset-self.timeline_width/2
            mainline = line(ox,oy,ox+self.width,oy,self.colour,self.timeline_width)
        else:
            ox = ox + self.timeline_offset + self.timeline_width/2
            mainline = line(ox,oy,ox,oy+self.height,self.colour,self.timeline_width)

        diagram.add(mainline)

        timeline_pos = None

        last_label_location = None
        for idx in range(len(self.elements)):
            (dt,e,label,offset) = self.elements[idx]
            if dt:
                pos = self.getUnixTime(dt)

            ew = 0
            eh = 0

            if e:
                ew = e.getWidth()
                eh = e.getHeight()

            if self.horizontal:
                xc = ox+ew/2
                if idx == 0:
                    timeline_pos = xc
                yc = oy-offset-eh/2
                if e:
                    e.draw(diagram,xc,yc)
                ox += ew
                if e:
                    ox += self.spacing
                if dt:
                    x1 = timeline_pos + (pos-self.start_pos)*self.pps
                    y1 = oy
                    x2 = xc
                    y2 = oy - offset
                    cp1 = (x1,y2)
                    cp2 = (x2,y1)
                    if label:
                        txt = text(x1,y1+self.timeline_width/2+self.label_space,label)
                        txt.addAttrs(self.text_attributes)
                        txt.addAttr("text-anchor","middle")
                        diagram.add(txt)
            else:
                yc = oy+eh/2
                if idx == 0:
                    timeline_pos = yc
                xc = ox+offset+ew/2
                if e:
                    e.draw(diagram,xc,yc)
                oy += eh
                if e:
                    oy += self.spacing
                if dt:
                    x1 = ox
                    y1 = timeline_pos + (pos-self.start_pos)*self.pps
                    x2 = ox + offset
                    y2 = yc
                    cp1 = (x2,y1)
                    cp2 = (x1,y2)
                    if label:
                        if last_label_location is None or abs(y1-last_label_location) > self.text_font_height*1.5:
                            # avoid drawing overlapping labels
                            txt = text(x1-self.timeline_width/2-self.label_space,y1,label)
                            txt.addAttrs(self.text_attributes)
                            txt.addAttr("text-anchor","end")
                            txt.setVerticalCenter()
                            diagram.add(txt)
                            last_label_location = y1
            if dt:
                c1 = circle(x1,y1,self.timeline_width,self.colour)
                diagram.add(c1)
                if e:
                    if self.horizontal:
                        s1 = sector(x2,y2,0,self.timeline_width,-math.pi,0,fill=self.colour)
                    else:
                        s1 = sector(x2,y2,0,self.timeline_width,-math.pi/2,math.pi/2,fill=self.colour)
                    diagram.add(s1)
                    branch = cubic_bezier((x1,y1),cp1,cp2,(x2,y2),self.colour,self.timeline_width)
                    diagram.add(branch)
