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

import json

from visigoth.utils.fonts.fontmanager import FontManager
from visigoth.svg import text, tspan
from visigoth.common.diagram_element import DiagramElement

class Text(DiagramElement):
    """
    Create a text string

    Arguments:
        
    Keyword Arguments:
        text_or_list(str) : str or list of Span or str 
        max_width(int) : maximum width for text, wrap to multiple lines 
        font_height(int) : font size in pixels
        text_attributes(dict): a dict containing SVG name/value attributes
        url(str): url to link to from the text
        line_spacing(int): spacing between line in pixels
    """

    def __init__(self,text_or_list="",max_width=None,font_height=24,text_attributes={},url=None,line_spacing=None):
        DiagramElement.__init__(self)
        self.built = False
        self.text_or_list = text_or_list
        self.max_width = max_width
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.url = url
        self.line_spacing = line_spacing
        self.width = 0
        self.height = 0
        
    def build(self):
        if self.built:
            return

        self.built = True
        self.lines = [] # list of (text,[span,...]) pairs
        self.tspans = []

        if isinstance(self.text_or_list,str):
            self.tspans = [Span(self.text_or_list,font_height=self.font_height, text_attributes=self.text_attributes,url=self.url)]
        else:
            self.tspans = []
            for item in self.text_or_list:
                if isinstance(item,str):
                    self.tspans.append(Span(item,font_height=self.font_height, text_attributes=self.text_attributes))
                else:
                    if not item.getHeight():
                        item.setHeight(self.font_height)
                    self.tspans.append(item)

        for ts in self.tspans:
            ts.build()
        
        tspans = self.tspans[:]
        outline = []

        i = 0
        while i<len(tspans):
            tspan = tspans[i]
            outspan = Span("",text_attributes=tspan.text_attributes,font_height=tspan.font_height,url=tspan.url)
            textstr = tspan.textstr
            buffer = ""
            j = 0
            while j < len(textstr):
                ch = textstr[j]
                buffer += ch
                if ch == ' ' or j == len(textstr)-1:        
                    bw = FontManager.getTextLength(outspan.text_attributes,buffer,outspan.font_height)
                    linew = bw + outspan.getWidth()+sum([ts.getWidth() for ts in outline])
                    if not self.max_width or linew <= self.max_width:
                        outspan.appendText(buffer)
                        outspan.build()
                        buffer = ""
                    else:
                        if not outline and not outspan.getText():
                            # edge case - forced to break a word across lines
                            buffer = ""
                            j = 1
                            while j < len(textstr):
                                w = FontManager.getTextLength(tspan.text_attributes,textstr[:j],tspan.font_height)
                                if w > self.max_width:
                                    j -= 1
                                    break
                                j += 1
                            outspan.setText(textstr[:j+1])
                        outspan.build()
                        outline.append(outspan)
                        self.lines.append(outline)
                        outspan = Span("",text_attributes=tspan.text_attributes,font_height=tspan.font_height,url=tspan.url)
                        outline = []
                        newspan = Span(buffer+textstr[j+1:],text_attributes=tspan.text_attributes,font_height=tspan.font_height,url=tspan.url)
                        newspan.build()
                        tspans.insert(i+1,newspan)
                        break
                j += 1        
            if outspan.getText():
                outspan.build()
                outline.append(outspan)    
            i += 1
            
        if outline:
            self.lines.append(outline)
            
        self.height = 0
        self.width = 0
        for  nr in range(len(self.lines)):
            tspans = self.lines[nr]
            tspans[0].lstrip()
            tspans[-1].rstrip()
            tspans = [ts for ts in tspans if ts.getText()]
            for t in tspans:
                t.build()
            h = max([t.getHeight() for t in tspans])
            w = sum([t.getWidth() for t in tspans])

            self.height += h
            self.width = max(w,self.width)
            self.lines[nr] = (tspans,w,h)
   
        if len(self.lines) > 1 and self.line_spacing:
            self.height = self.lines[0][2]/2 + self.line_spacing * (len(self.lines)-1) + self.lines[-1][2]/2

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def draw(self,d,cx,cy):
        og = d.openGroup(self.getId())
        y = cy - self.height/2
        ox = cx - self.width/2
        g = d.openGroup()
        for i in range(len(self.lines)):
            (tspans,w,h) = self.lines[i]
            if i == 0 or not self.line_spacing:
                y += h/2
            else:
                y += self.line_spacing/2
            tx = ox
            for tt in tspans:
                tx += tt.getWidth()/2    
                tt.draw(d,tx,y)
                tx += tt.getWidth()/2
            if self.line_spacing:
                y += self.line_spacing/2
            else:
                y += h/2
        d.closeGroup()
        d.closeGroup()
        return g

class Span(object):

    """
    Create a Span to describe a section of a larger text with specific attributes

    Arguments:
        
    Keyword Arguments:
        textstr(str) : the text
        font_height(int) : font size in pixels
        text_attributes(dict): a dict containing SVG name/value attributes
        url(str): url to link to from the text
    """
    
    def __init__(self,textstr="",font_height=0,text_attributes={},url=None):
        self.textstr = textstr
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.url = url
        self.width = 0
        self.height = 0

    def __repr__(self):
        return "["+self.textstr+"]"

    def setText(self,text):
        self.textstr = text

    def appendText(self,text):
        self.textstr += text

    def getText(self):
        return self.textstr

    def lstrip(self):
        self.textstr = self.textstr.lstrip()

    def rstrip(self):
        self.textstr = self.textstr.rstrip()
        
    def build(self):
        self.width = FontManager.getTextLength(self.text_attributes,self.textstr,self.font_height)
        
    def getHeight(self):
        return self.font_height

    def setHeight(self,height):
        self.font_height = height

    def getWidth(self):
        return self.width

    def draw(self,d,cx,cy):
        ts = text(cx,cy,self.textstr,font_height=self.font_height,text_attributes=self.text_attributes)
        ts.setVerticalCenter()
        if self.url:
            ts.setUrl(self.url)
        d.add(ts)
