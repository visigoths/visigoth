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

import time
import math

from visigoth.common import DiagramElement
from visigoth.utils.fonts import FontManager
from visigoth.svg import text, line, circle, sector, cubic_bezier

class TimeLine(DiagramElement):

    def __init__(self, timeline_width=10, font_height=24, orientation="vertical", branch_length=100, spacing=20, colour="grey", text_attributes={}):
        """
        Create a TimeLine

        :param text_attributes: dict containing attributes to a apply to SVG text elements
        """
        DiagramElement.__init__(self)
        self.text_attributes = text_attributes
        self.elements = []
        self.timeline_width = timeline_width
        self.horizontal = False
        if orientation == "horizontal":
            self.horizontal = True
        self.branch_length = branch_length
        self.spacing = spacing
        self.colour = colour
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

    def build(self):
        if len(self.elements) == 0:
            return

        lstart = 0
        lend = 0
        length = 0
        depth = 0
        label_wh = 0
        start_dt = None
        end_dt = None
        first_e = None
        for index in range(len(self.elements)):
            (dt,e,label,offset) = self.elements[index]

            w = 0
            h = 0
            if e:
                e.build()
                w = e.getWidth()
                h = e.getHeight()
                if not first_e:
                    first_e = e

            if self.horizontal:
                th = 0
                if label:
                    th = self.text_font_height
                label_wh = max(label_wh,th)
                l = h
                d = w + offset + self.timeline_width + self.label_space + th
                self.timeline_offset = max(self.timeline_offset,self.label_space + th)
            else:
                tw = 0
                if label:
                    tw = FontManager.getTextLength(self.text_attributes,label,self.text_font_height)
                label_wh = max(tw,label_wh)
                l = w
                d = h + offset + self.timeline_width + self.label_space + tw
                self.timeline_offset = max(self.timeline_offset,self.label_space + tw)

            if dt != None and start_dt == None:
                lstart = length + l/2
                start_dt = dt

            if e and e != first_e:
                length += self.spacing

            if dt != None:
                lend = length + l/2
                end_dt = dt

            length += l
            depth = max(depth,d)

        self.start_pos = self.getUnixTime(start_dt)
        self.end_pos = self.getUnixTime(end_dt)

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
                xc = ox+offset+eh/2
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
                        txt = text(x1-self.timeline_width/2-self.label_space,y1,label)
                        txt.addAttrs(self.text_attributes)
                        txt.addAttr("text-anchor","end")
                        txt.setVerticalCenter()
                        diagram.add(txt)
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
