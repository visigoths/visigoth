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
from visigoth.svg import polygon

import math

class Palette(object):

    def __init__(self,defaultColour):
        self.defaultColour = Colour.toHEX(defaultColour)

    def getDefaultColour(self):
        return self.defaultColour

    def setDefaultColour(self,defaultColour):
        self.defaultColour = Colour.toHEX(defaultColour)


class DiscretePalette(Palette):

    def __init__(self,colourMap="pastel",defaultColour="gray"):
        """
        Create a palette mapping discrete values to colours

        Arguments:
            colourMap(str): the name of a colourMap (see Notes) OR a list of colour names

        Keyword Arguments:
            defaultColour(str): the name of the default colour to use (to represent mpy values)

        Notes:
            A list of the names and numbers of colours in each map is:

            "deep": 10
            "deep6": 6
            "muted": 10
            "muted6": 6
            "pastel": 10
            "pastel6": 6
            "bright": 10
            "bright6": 6
            "dark": 10
            "dark6": 6
            "colorblind": 10
            "colorblind6":6
        """
        super(DiscretePalette,self).__init__(defaultColour)
        self.built = False
        self.categories = []
        self.categorylist = []
        self.colourMap = DiscreteColourMaps[colourMap] if colourMap else None
        self.opacity = 1.0
        self.value_labels = {}
        self.colour_lookup = {}

    @staticmethod
    def listColourMaps():
        return sorted(DiscreteColourMaps.keys())

    def isDiscrete(self):
        return True

    def addColour(self,category,colour,label=None):
        if label is None:
            label = str(category)
        self.categories.append((category,colour))
        self.categorylist.append(category)
        self.value_labels[category] = label
        return self

    def getCategories(self):
        return self.categories

    def allocateColour(self,value):
        if value is not None:
            if value not in self.categorylist:
                self.categorylist.append(value)

    def build(self):
        # build a colour lookup table
        if not self.built:
            final_categories=[]
            for (cat,col) in self.categories:
                col = Colour.applyOpacity(col, self.opacity)
                self.colour_lookup[cat] = col
                final_categories.append((cat,col))

            # assign colours to all unassigned categories from the colour map
            cm_index = 0
            for category in self.categorylist:
                if category not in self.colour_lookup:
                    if not self.colourMap:
                        raise Exception("Please define a colour map")
                    col = self.colourMap[cm_index]
                    col = Colour.applyOpacity(col, self.opacity)
                    self.colour_lookup[category] = col
                    cm_index += 1
                    cm_index = cm_index % len(self.colourMap)
                    final_categories.append((category,col))

            self.categories = final_categories
            # apply opacity to the default colour
            self.setDefaultColour(Colour.applyOpacity(self.getDefaultColour(),self.opacity))
            self.built = True

    def getColour(self,value):
        if value is None:
            return self.getDefaultColour()
        else:
            if value in self.colour_lookup:
                return self.colour_lookup[value]
            else:
                return self.getDefaultColour()

    def getLabel(self,value):
        return self.value_labels.get(value,str(value))

    def setOpacity(self,opacity):
        self.opacity = opacity

    def getOpacity(self):
        return self.opacity

class ContinuousPalette(Palette):

    def __init__(self, colourMap="viridis", withIntervals=True, intervals=[], defaultColour="gray",min_val=None,max_val=None,undershootColour=None,overshootColour=None):
        """
        Create a palette mapping continuous values to colours

        KeywordArguments:
            colourMap(str): the name of a predefined colorMap to use (see Notes) or a list of colour names
            withIntervals(boolean): whether the colour range should be divided into a smallish number of intervals
            intervals(list): manually define list of values in ascending order defining the intervals
            defaultColour(str): the name of the default colour to use (to represent mpy values)
            min_val(float): manually set a minimum value (use the minimum from the data if not provided)
            max_val(float): manually set a maximum value (use the maximum from the data if not provided)
            undershootColour(str): the colour to use for values below a manually set minimum value
            overshootColour (str): the colour to use for values above a manually set maximum value
        """
        super(ContinuousPalette,self).__init__(defaultColour)
        self.undershootColour=Colour.toHEX(undershootColour)
        self.overshootColour=Colour.toHEX(overshootColour)
        self.colour = None
        self.range = []
        self.withIntervals = withIntervals
        self.intervals = []
        self.rescaled = False
        self.colourMap = None
        self.cap_size = 10
        self.tickpositions = intervals
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

    def getCapSize(self):
        return self.cap_size

    def getUndershootColour(self):
        return self.undershootColour if self.undershootColour is not None else self.getColour(self.min_value)

    def getOvershootColour(self):
        return self.overshootColour if self.overshootColour is not None else self.getColour(self.max_value)

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

    def getTickPositions(self):
        return self.tickpositions

    def setIntervals(self):
        self.colour = Colour(self.range,self.min_value,self.max_value)
        # work out the lower and upper bounds of the value range
        lwb = self.min_value
        upb = self.max_value
        # take tickpositions into account, if the caller has set them
        if self.tickpositions:
            lwb = min(lwb,self.tickpositions[0])
            upb = max(upb,self.tickpositions[-1])
        axisutils = AxisUtils(100,"vertical",lwb,upb)
        if self.tickpositions:
            axisutils.setTickPoints(self.tickpositions)
        ticks = axisutils.build()
        lwb = ticks[0]
        upb = ticks[-1]
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
        self.colour = Colour(self.intervals,lwb,upb)
        self.min_value = lwb
        self.max_value = upb

    def getIntervals(self):
        return self.intervals

    def allocateColour(self,value):
        if not self.fixed_min_value:
            if self.min_value == None or value < self.min_value:
                self.min_value = value
        if not self.fixed_max_value:
            if self.max_value == None or value > self.max_value:
                self.max_value = value

    def getColour(self,value):
        if value is None or math.isnan(value):
            return self.getDefaultColour()
        elif value < self.min_value:
            return self.getUndershootColour()
        elif value > self.max_value:
            return self.getOvershootColour()
        elif self.colour:
            return self.colour.getColour(value)
        else:
            return None

    def drawColourRectangle(self,doc,x,y,width,height,orientation,stroke_width=None,stroke=None):
        if orientation == "horizontal":
            rx = x + self.cap_size
            ry = y
            rwidth = width - 2*self.cap_size
            rheight  = height
        else:
            rx = x
            ry = y + self.cap_size
            rwidth = width
            rheight = height  - 2 * self.cap_size

        self.colour.drawColourRectangle(doc,rx,ry,rwidth,rheight,orientation,stroke_width=stroke_width,stroke=stroke)
        xmin = rx
        xmax = rx+rwidth
        ymin = ry
        ymax = ry+rheight
        if orientation == "horizontal":
            p1 = polygon([(xmin,ymin),(xmin,ymax),(xmin-10,y+rheight/2)],fill=self.getUndershootColour(),stroke=stroke, stroke_width=stroke_width)
            p2 = polygon([(xmax, ymin), (xmax, ymax), (xmax + 10, y+rheight/2)], fill=self.getOvershootColour(),stroke=stroke, stroke_width=stroke_width)
        else:
            p1 = polygon([(xmin, ymin), (xmax, ymin), (xmin + rwidth / 2,ymin - 10)], fill=self.overshootColour,
                         stroke=stroke, stroke_width=stroke_width)
            p2 = polygon([(xmin, ymax), (xmax, ymax), (xmin + rwidth/2, ymax + 10)], fill=self.undershootColour,
                         stroke=stroke, stroke_width=stroke_width)
        p1.addAttr("stroke-linejoin","round")
        doc.add(p1)
        p2.addAttr("stroke-linejoin", "round")
        doc.add(p2)

