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

import random
from visigoth.charts import ChartElement
from math import radians,sin,cos,pi,sqrt
import sys

# import numpy
from visigoth.common.diagram_element import DiagramElement
from visigoth.svg import text, rectangle
from visigoth.utils.fonts import FontManager
from visigoth.utils.term.progress import Progress

class WordCloud(ChartElement):

    def __init__(self, data, width, height, palette, text_attributes={},seed=None,flip_fraction=0.1,fill="white"):
        """
        Add a WordCloud to the section

        Arguments:
            data(list) : data describing a document in the form of a list of items, where each item is a tuple (word,category,value)
            width(int) : the width of the plot in pixels
            height(int) : the height of the plot in pixels
            palette(list) : a list of (category, colour) pairs

        Keyword Arguments:
            text_attributes(dict) : dict containing attributes to a apply to SVG text elements
            seed(int) : random seed - set to produce repeatable results
            flip_fraction(float) : fraction of words (between 0.0 and 1.0) to display vertically
            fill(str) : colour to use as text background

        :return: a WordCloud object
        """
        super(WordCloud, self).__init__()
        self.data = data
        self.width = width
        self.height = height
        self.palette = palette
        self.total = sum([v for (word,cat,v) in data])
        self.plots = []
        self.renders = []
        self.text_attributes = text_attributes
        self.flip_fraction = flip_fraction
        self.positions = {} # True|False => Int, record the last insertion positions for horizontal and vertical text
        self.margin = 0.9
        self.fill = fill

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def build(self):
        cx = 0
        cy = 0

        oy = cy - self.height/2
        ox = cx

        xc = ox - self.width/2
        yc = oy
        counter = 0
        p = Progress("WordCloud")

        for (word,cat,v) in sorted(self.data,key=lambda x:x[2],reverse=True):
            counter += 1
            frac = v/self.total
            a = self.width * self.height * frac * 0.5
            l = len(word)
            h = sqrt(a/l)
            w = FontManager.getTextLength(self.text_attributes,word,h)

            sa = random.random()*pi
            sx = xc+self.width/2 # +sin(sa)*self.width/8
            sy = yc+self.height/2 # +cos(sa)*self.height/8

            flip = random.random()<self.flip_fraction

            if flip:
                w,h = h,w

            pos = self.positions.get(flip,0)

            while True:
                pos += 1
                coords = self.spiral(pos,sx,sy)
                if not coords:
                    break
                (x,y) = coords

                x = x-w/2
                y = y-h/2
                if not self.intersects(x,y,w,h):
                    self.plots.append((x,y,w,h))
                    self.renders.append((word,w,h,cat,x,y,flip))
                    self.positions[flip] = pos
                    break
            
            p.report("Processing",counter/len(self.data))
        
        maxx = None
        maxy = None
        minx = None
        miny = None
        for (_,w,h,_,x,y,flip) in self.renders:
            if flip:
                ww = h
                hh = w
            else:
                ww = w
                hh = h
            if miny == None or y - hh/2 < miny:
                miny = y - hh/2
            if minx == None or x - ww/2 < minx:
                minx = x - ww/2
            if maxy == None or y + hh/2 > maxy:
                maxy = y + hh/2
            if maxx == None or x + ww/2 > maxx:
                maxx = x + ww/2

        wratio = (maxx-minx) / self.width
        hratio = (maxy-miny) / self.height
        ratio = max(hratio,wratio)

        ratio = 1/ratio
        ratio *= 0.95
        
        self.renders = [(word,ratio*w,ratio*h,cat,x*ratio,y*ratio,flip) for (word,w,h,cat,x,y,flip) in self.renders]

        p.complete("Complete")

    def drawChart(self,doc,cx,cy,chart_width,chart_height):
        categories = {}
        for (word,w,h,cat,x,y,flip) in self.renders:
            col = self.getColour(cat)
            cid = self.plotWord(doc,word,w,h,col,x+cx,y+cy,flip)
            ids = categories.get(cat,[])
            ids.append(cid)
            categories[cat] = ids
        return {"categories":categories}

    def getColour(self,cat):
        return self.palette.getColour(cat)

    def plotWord(self,doc,word,w,h,col,x,y,flip):
        g = doc.openGroup()
        gid = g.getId()
        r = rectangle(x,y,w,h,fill=self.fill)
        doc.add(r)
        if flip:
            fs = w
            tl = h
        else:
            fs = h
            tl = w
        
        fs *= self.margin
        tl *= self.margin

        t = text(x+w*0.5,y+h*0.5,word)
        t.setHorizontalCenter()
        t.setVerticalCenter()
        t.addAttr("font-size",fs)
        t.addAttr("fill",col)
        t.addAttrs(self.text_attributes)
        if flip:
            t.addAttr("writing-mode","tb")
        doc.add(t)
        doc.closeGroup()
        return gid

    def spiral(self,pos,cx,cy):
        angle = (pos/100)*pi
        r = pos/50
        if r > self.width/2 or r >self.height/2:
            return None
        return (cx+r*sin(angle),cy+r*cos(angle))

    def intersects(self,x1,y1,w1,h1):
        for area in self.plots:
            (x2,y2,w2,h2) = area
            if not (x1 > x2+w2 or x1+w1 < x2 or y1 > y2+h2 or y1+h1 < y2):
                return True
        return False

