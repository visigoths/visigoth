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

from visigoth.utils.colour.colour import Colour, ColourException
from visigoth.common.axis import AxisUtils
from visigoth.utils.colour.colourmaps import ColourMaps, DiscreteColourMaps

class Palette(object):

    def __init__(self,defaultColour):
        self.defaultColour = defaultColour

    def getDefaultColour(self):
        return self.defaultColour

    def setDefaultColour(self,defaultColour):
        self.defaultColour = Colour.toHEX(defaultColour)


class DiscretePalette(Palette):

    def __init__(self,colourMap="pastel",defaultColour="white"):
        super(DiscretePalette,self).__init__(defaultColour)
        self.colour = None
        self.categories = []
        self.categoryset = set()
        self.colourMap = colourMap
        self.opacity = 1.0

    def build(self):
        pass
        
    @staticmethod
    def listColourMaps():
        return sorted(DiscreteColourMaps.keys())

    def isDiscrete(self):
        return True

    def addColour(self,category,colour):
        self.categories.append((category,colour))
        self.categoryset.add(category)
        return self

    def getCategories(self):
        return self.categories

    def getColour(self,value):
        if self.colour == None:
            self.colour = Colour(self.categories,colourMap=self.colourMap)
            self.colour.setOpacity(self.opacity)
        if value is None:
            return self.getDefaultColour()
        try:
            # if the value already represents a valid colour, use that colour
            Colour.parseColour(value)
            col = value
        except ColourException:
            # assign a new colour from the colour map, if necessary
            col = self.colour.getColour(value)
        if value not in self.categoryset:
            self.categoryset.add(value)
            self.categories.append((value,col))
        return col

    def setOpacity(self,opacity):
        self.opacity = opacity
        if self.colour:
            self.colour.setOpacity(opacity)

    def getOpacity(self):
        return self.opacity

class ContinuousPalette(Palette):

    def __init__(self, withIntervals=True, colourMap="viridis", defaultColour="white",min_val=None,max_val=None):
        super(ContinuousPalette,self).__init__(defaultColour)
        self.colour = None
        self.range = []
        self.withIntervals = withIntervals
        self.intervals = []
        self.rescaled = False
        self.colourMap = None

        self.fixed_min_value=min_val is not None
        self.min_value = min_val

        self.fixed_max_value = max_val is not None
        self.max_value = max_val

        if isinstance(colourMap,str):
            if colourMap not in ColourMaps:
                raise Exception("Unknown colourmap %s"%(colourMap))
            colourMap = ColourMaps[colourMap]

        self.colourMap = colourMap
        for i in range(len(self.colourMap)):
            entry = self.colourMap[i]
            if isinstance(entry,list) or isinstance(entry,tuple):
                r = self.colourMap[i][0]
                g = self.colourMap[i][1]
                b = self.colourMap[i][2]
                self.__appendColour("#%02X%02X%02X"%(int(255*r),int(255*g),int(255*b)),i)
            else:
                self.__appendColour(entry,i)

    @staticmethod
    def listColourMaps():
        return sorted(ColourMaps.keys())

    def __repr__(self):
        return str(self.range)

    def isDiscrete(self):
        return False

    def __appendColour(self,colour,value):
        self.range.append((value,colour))
        self.range = sorted(self.range,key = lambda x:x[0])

    def getMinValue(self):
        return self.min_value

    def getMaxValue(self):
        return self.max_value

    def build(self):
        # if no values have been set, set some dummy ones
        if self.min_value == None:
            self.min_value = 0
        if self.max_value == None:
            self.max_value = 0
        # make sure max is > min
        if self.max_value <= self.min_value:
            self.max_value = self.min_value + 1
        # set the domain of the colour range linearly from min to max
        for idx in range(0,len(self.range)):
            frac = idx / (len(self.range)-1)
            val = self.min_value + (frac * (self.max_value-self.min_value))
            self.range[idx] = (val,self.range[idx][1])
        #
        if self.withIntervals:
            self.setIntervals()
        else:
            self.colour = Colour(self.range,self.min_value,self.max_value)

    def setIntervals(self):
        self.colour = Colour(self.range,self.min_value,self.max_value)
        lwb = self.min_value
        upb = self.max_value

        axisutils = AxisUtils(100,"vertical",self.min_value,self.max_value)
        ticks = axisutils.build()
        self.intervals = []
        # intervals will be a list of (val0,val1,col) associating colour col with values in the range v >= val0 and v < val1
        for idx in range(len(ticks)):
            val = ticks[idx]
            if idx == 0 and val > lwb:
                col = self.colour.getColour(lwb + (val-lwb)/2)
                self.intervals.append((lwb,val,col))
            if idx > 0:
                val0 = ticks[idx-1]
                val1 = ticks[idx]
                col = self.colour.getColour(val0 + (val1-val0)/2)
                self.intervals.append((val0,val1,col))
            if idx == len(ticks)-1 and val < upb:
                col = self.colour.getColour(val + (upb - val) / 2)
                self.intervals.append((val, upb, col))
        self.colour = Colour(self.intervals,self.min_value,self.max_value)

    def getIntervals(self):
        return self.intervals

    def getColour(self,value):
        if value is None:
            return self.getDefaultColour()
        if not self.fixed_min_value:
            if self.min_value == None or value < self.min_value:
                self.min_value = value
        if not self.fixed_max_value:
            if self.max_value == None or value > self.max_value:
                self.max_value = value
        if self.colour:
            return self.colour.getColour(value)
        else:
            return None

    def drawColourRectangle(self,doc,x,y,width,height,orientation,stroke_width=None,stroke=None):
        return self.colour.drawColourRectangle(doc,x,y,width,height,orientation,stroke_width=stroke_width,stroke=stroke)
