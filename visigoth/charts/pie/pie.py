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

import math
import json

from visigoth.charts import ChartElement
from visigoth.svg import sector, text
from visigoth.utils.fonts.fontmanager import FontManager

class Pie(ChartElement):
    """
    Create a Hierarchical Pie/Doughnut Chart

    Args:
        data (dict): A list containing (category,value) pairs where value may be a numeric value or a nested list.
        width (int): the width of the plot in pixels
        height (int): the height of the plot in pixels
        palette(list) : a list of (category, colour) pairs

    Keyword Args:
        stroke (str): stroke color for pie sectors
        stroke_width (int): stroke width for pie sectors
        doughnut (boolean): set True to draw as a doughnut rather than a pie chart
        labelfn (lambda): function to compute a label string, given a category and numeric value
        font_height (int): sets the maximum font height used to display labels
        text_attributes (dict): attributes to apply to text labels
    """
    def __init__(self,data,width,height,palette,stroke="black",stroke_width=2,doughnut=False,labelfn=lambda k,v:"%s:%0.1f"%(k,v),font_height=20,text_attributes={}):
        super(Pie, self).__init__()
        self.data = data
        self.levels = self.countLevels(data)
        self.width = width
        self.height = height
        self.palette = palette
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.doughnut = doughnut
        self.labelfn = labelfn
        self.font_height = font_height
        self.text_attributes = text_attributes

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def build(self):
        pass

    def countLevels(self,d):
        if isinstance(d,list):
            return 1+max([self.countLevels(v) for (k,v) in d])
        else:
            return 0

    def getCount(self,d):
        if isinstance(d,list):
            return sum([self.getCount(v) for (k,v) in d])
        else:
            return d

    def getLevel(self,indices,data):
        if not indices:
            return list(map(lambda x:(x[0],self.getCount(x[1])),data))
        else:
            idx = indices[0]
            (k,v) = data[idx]
            if isinstance(v,list):
                return self.getLevel(indices[1:],v)
            else:
                return None

    def drawChart(self,doc,cx,cy):
        config = { "categories": {} }
        levels = self.countLevels(self.data)
        if self.doughnut:
            levels += 1

        # compute the radius of each level (ring) in the chart
        self.rlevel = min(self.height/2,self.width/2)/levels
        self.drawLevel(doc,cx,cy,[],0.0,2*math.pi,config)
        return config

    def drawLevel(self,doc,cx,cy,indices,thetaMin,thetaMax,config):
        theta = thetaMin
        level = len(indices)+1
        levelData = self.getLevel(indices,self.data)
        if levelData == None:
            return

        if self.doughnut:
            level += 1

        data_sum = sum([v for (k,v) in levelData])
        if self.labelfn:
            # max_label_len = max([len(self.labelfn(k,v)) for (k,v) in levelData])
            max_label_width = max([FontManager.getTextLength(self.text_attributes,self.labelfn(k,v),self.font_height) for (k,v) in levelData])
            
            font_height = min(self.font_height,self.font_height*(self.rlevel/max_label_width))

        for idx in range(len(levelData)):
            (k,v) = levelData[idx]
            theta0 = theta
            theta += (thetaMax-thetaMin)*v/data_sum
            self.drawLevel(doc,cx,cy,indices+[idx],theta0,theta,config)
            col = self.palette.getColour(k)
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


