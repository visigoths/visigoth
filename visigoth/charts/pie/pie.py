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

import math
import json

from visigoth.charts import ChartElement
from visigoth.svg import sector, text
from visigoth.utils.fonts.fontmanager import FontManager
from visigoth.utils.data import Dataset
from visigoth.utils.colour import DiscreteColourManager

class Pie(ChartElement):
    """
    Create a Hierarchical Pie/Doughnut Chart

    Args:
        data (dict): A relational data set (for example, list of dicts/lists/tuples describing each row)
        
    Keyword Args:
        value (str or int): Identify the column to specify the value (use count if not specified)
        colour (str or int): Identify the column to define the sector colour (provide a list to create a multi-level pie chart)
        width (int): the width of the plot in pixels
        height (int): the height of the plot in pixels
        colour_manager(list) : a DiscreteColourManager object
        stroke (str): stroke color for pie sectors
        stroke_width (int): stroke width for pie sectors
        doughnut (boolean): set True to draw as a doughnut rather than a pie chart
        labelfn (lambda): function to compute a label string, given a category and numeric value
        font_height (int): sets the maximum font height used to display labels
        text_attributes (dict): attributes to apply to text labels
    """
    def __init__(self,data,value=0,colour=1,width=768,height=768,colour_manager=None,stroke="black",stroke_width=2,doughnut=False,labelfn=lambda k,v:"%s:%0.1f"%(k,v),font_height=20,text_attributes={}):
        super(Pie, self).__init__()
        self.data = Dataset(data)
        self.value = value
        self.colour = colour
        if not isinstance(self.colour,list):
            self.colour = [self.colour]
        self.levels = len(self.colour)
        self.width = width
        self.height = height
        if not colour_manager:
            colour_manager = DiscreteColourManager()
        self.setPalette(colour_manager)
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.doughnut = doughnut
        self.labelfn = labelfn
        self.font_height = font_height
        self.text_attributes = text_attributes

        for colour in self.colour:
            cats = self.data.query([colour],unique=True,flatten=True)
            for cat in cats:
                self.getPalette().allocateColour(cat)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def build(self,fmt):
        pass

    def getCount(self,d):
        if isinstance(d,list):
            return sum([self.getCount(v) for (k,v) in d])
        else:
            return d

    def getLevel(self,parentcolours,data):
        if not self.colour:
            if parentcolours == []:
                return self.data.query([str(self.value),self.value])

        if not self.colour or len(parentcolours) == len(self.colour):
            return None # indicates no more levels

        qfilters = []
        level = len(parentcolours)
        for (colourcol,parentcolour) in zip(self.colour,parentcolours):
            qfilters.append(Dataset.filter(colourcol,"=",parentcolour))
        levelcolour = self.colour[level]
        if self.value:
            aggregation = Dataset.sum(self.value)
        else:
            aggregation = Dataset.count()
        return self.data.query([levelcolour],aggregations=[aggregation],filters=qfilters)

    def drawChart(self,doc,cx,cy,cwidth,cheight):
        config = { "categories": {} }
        levels = self.levels
        if self.doughnut:
            levels += 1

        # compute the radius of each level (ring) in the chart
        self.rlevel = min(self.height/2,self.width/2)/levels
        self.drawLevel(doc,cx,cy,[],0.0,2*math.pi,config)
        return config

    def drawLevel(self,doc,cx,cy,parentcolours,thetaMin,thetaMax,config):
        theta = thetaMin
        level = len(parentcolours)+1
        if self.doughnut:
            level += 1

        levelData = self.getLevel(parentcolours,self.data)
        if not levelData:
            return

        levelData = list(filter(lambda x:x[0],levelData))
        
        if not levelData:
            return

        data_sum = sum([v for (k,v) in levelData])
        if self.labelfn:
            max_label_width = max([FontManager.getTextLength(self.text_attributes,self.labelfn(k,v),self.font_height) for (k,v) in levelData])            
            font_height = min(self.font_height,self.font_height*(self.rlevel/max_label_width))

        for idx in range(len(levelData)):
            (k,v) = levelData[idx]
            theta0 = theta
            theta += (thetaMax-thetaMin)*v/data_sum
            self.drawLevel(doc,cx,cy,parentcolours+[k],theta0,theta,config)
            col = self.getPalette().getColour(k)
            tooltip = self.getTooltip(k,v)
            r = level*self.rlevel
            s = sector(cx,cy, r-self.rlevel, r, theta0, theta, tooltip)
            s.addAttr("fill",col)
            s.addAttr("stroke",self.stroke)
            s.addAttr("stroke-width",self.stroke_width)
            config["categories"][k] = [s.getId()]
            doc.add(s)
            if self.labelfn:
                angle = (theta+theta0)/2.0
                r = (r-self.rlevel/2.0)
                tx = cx+r*-math.cos(angle)
                ty = cy+r*-math.sin(angle)
                t = text(tx,ty,self.labelfn(k,v),tooltip,font_height,self.text_attributes)
                t.addAttrs(self.text_attributes)
                t.setVerticalCenter()
                if angle > math.pi*0.5 and angle < math.pi*1.5:
                    # reverse text angle to avoid text reading backwards
                    angle = angle + math.pi
                t.setRotation(angle)
                doc.add(t)


