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

from visigoth.utils.colour import Colour
from visigoth.common.axis import AxisUtils
from visigoth.utils.colour.colourmaps import ColourMaps, DiscreteColourMaps


class Palette(object):

    def __init__(self,defaultColour):
        self.defaultColour = defaultColour

    def getDefaultColour(self):
        return self.defaultColour

    def setDefaultColour(self,defaultColour):
        self.defaultColour = defaultColour

class DiscretePalette(Palette):

    def __init__(self,colourMap="pastel",defaultColour="blue"):
        super(DiscretePalette,self).__init__(defaultColour)
        self.colour = None
        self.categories = []
        self.categoryset = set()
        self.colourMap = colourMap
        

    def build(self):
        pass
        
    @staticmethod
    def listColourMaps():
        return sorted(DiscreteColourMaps.keys())

    def isDiscrete(self):
        return True

    def addCategory(self,category,colour):
        self.categories.append((category,colour))
        self.categoryset.add(category)
        return self

    def getCategories(self):
        return self.categories

    def getColour(self,value):
        if self.colour == None:
            self.colour = Colour(self.categories,colourMap=self.colourMap)
        if not value:
            return self.colour.getDefaultColour()
        col = self.colour.getColour(value)
        if value not in self.categoryset:
            self.categoryset.add(value)
            self.categories.append((value,col))
        return col

class ContinuousPalette(Palette):

    def __init__(self, withIntervals=True,colourMap="viridis", defaultColour="blue"):
        super(ContinuousPalette,self).__init__(defaultColour)
        self.colour = None
        self.range = []
        self.withIntervals = withIntervals
        self.intervals = []
        self.rescaled = False
        self.colourMap = None
        self.min_value = None
        self.max_value = None
        self.built = False
        if colourMap:
            if colourMap not in ColourMaps:
                raise Exception("Unknown colourmap %s"%(colourMap))
            self.colourMap = ColourMaps[colourMap]
            for i in range(len(self.colourMap)):
                r = self.colourMap[i][0]
                g = self.colourMap[i][1]
                b = self.colourMap[i][2]
                self.appendColour("#%02X%02X%02X"%(int(255*r),int(255*g),int(255*b)),i)

    @staticmethod
    def listColourMaps():
        return sorted(ColourMaps.keys())

    def __repr__(self):
        return str(self.range)

    def isDiscrete(self):
        return False

    def build(self):
        if not self.built:
            self.rescaleTo(self.min_value,self.max_value)
        self.built = True

    def addColour(self,colour,value):
        # override preset colourMap
        if self.colourMap:
            self.colourMap = None
            self.range = []
            self.intervals = []
        self.appendColour(colour,value)
        return self

    def appendColour(self,colour,value):
        self.range.append((value,colour))
        self.range = sorted(self.range,key = lambda x:x[0])
        if len(self.range)>1 and self.withIntervals:
            self.setIntervals()
        else:
            self.colour = Colour(self.range)
        return self

    def getMinValue(self):
        return self.range[0][0]

    def getMaxValue(self):
        return self.range[-1][0]

    def rescaleTo(self,minval,maxval):
        if self.rescaled:
            return
        self.rescaled = True
        for idx in range(0,len(self.range)):
            frac = idx / (len(self.range)-1)
            val = minval + (frac * (maxval-minval))
            self.range[idx] = (val,self.range[idx][1])
        if self.withIntervals:
            self.setIntervals()
        else:
            self.colour = Colour(self.range)

    def setIntervals(self):
        self.colour = Colour(self.range)
        lwb = self.range[0][0]
        upb = self.range[-1][0]
        axisutils = AxisUtils(100,"vertical",lwb,upb)
        ticks = axisutils.build()
        self.intervals = []
        self.intervals.append((lwb,self.colour.getColour(lwb)))
        prev = lwb
        for val in ticks:
            delta = val - prev
            col = self.colour.getColour(val)
            self.intervals.append((max(val-delta/2,lwb),col))
            self.intervals.append((min(val+delta/2,upb),col))
            prev = val
        self.colour = Colour(self.intervals)

    def getColour(self,value):
        if self.min_value == None or value < self.min_value:
            self.min_value = value
        if self.max_value == None or value > self.max_value:
            self.max_value = value
        return self.colour.getColour(value)

    def drawColourRectangle(self,doc,x,y,width,height,orientation,stroke_width=None,stroke=None):
        return self.colour.drawColourRectangle(doc,x,y,width,height,orientation,stroke_width=stroke_width,stroke=stroke)
