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

import random
from visigoth.svg import rectangle, linear_gradient
from visigoth.utils.colour.webcolours import colours
from visigoth.utils.colour.colourmaps import DiscreteColourMaps

class Colour(object):

    webColours = { col["name"].lower():"#"+col["hex"] for col in colours }

    def __init__(self,palette,minValue=None,maxValue=None,defaultColour="red",colourMap=None):
        self.colourMap = colourMap
        self.colourMapIndex = 0
        self.palette = palette
        self.defaultColour = defaultColour
        self.palette_lookup = {}
        self.discrete = True
        if len(self.palette):
            if isinstance(self.palette[0][0],str):
                self.discrete = True
                self.palette_lookup = { cat:col for (cat,col) in self.palette }
            else:
                self.discrete = False
                if len(self.palette[0]) == 2:
                    self.palette_lookup = [(val,self.parseColour(col)) for (val,col) in self.palette]
                    self.gradients = True
                else:
                    self.gradients = False
                    self.palette_lookup = [(val0, val1, self.parseColour(col)) for (val0, val1, col) in self.palette]
        self.opacity = 1.0
        self.minValue = minValue
        self.maxValue = maxValue

    def getOpacity(self):
        return self.opacity

    def setOpacity(self,opacity):
        self.opacity = opacity

    def isDiscrete(self):
        return self.discrete

    def parseHex(self,s):
        return int(s,16)

    def parseColour(self,col):
        if col and (len(col) != 7 or col[0] != "#"):
            if col.lower() in Colour.webColours:
                col = Colour.webColours[col.lower()]
        if not col or col[0] != "#" or len(col) != 7:
            raise Exception("Unable to parse colour (%s)"%(col))
        r = self.parseHex(col[1:3])
        g = self.parseHex(col[3:5])
        b = self.parseHex(col[5:7])
        return (r,g,b)

    def computeColour(self,col1,col2,frac):
        r = col1[0]+int(frac*(col2[0]-col1[0]))
        g = col1[1]+int(frac*(col2[1]-col1[1]))
        b = col1[2]+int(frac*(col2[2]-col1[2]))
        return "#%02X%02X%02X"%(r,g,b)

    @staticmethod
    def randomColour(opacity=None):
        rng = random.Random()
        r = int(rng.random()*256)
        g = int(rng.random()*256)
        b = int(rng.random()*256)
        if opacity != None:
            o = int(opacity*256)
            return "#%02X%02X%02X%02X"%(r,g,b,o)
        else:
            return "#%02X%02X%02X"%(r,g,b)

    def getDefaultColour(self):
        return self.defaultColour

    def applyOpacity(self,colour):
        opacity = self.getOpacity()
        if opacity < 1.0:
            (r,g,b) = self.parseColour(colour)
            return "#%02X%02X%02X%02X"%(r,g,b,round(opacity*255))
        else:
            return colour

    def getColour(self,val):
        if self.discrete:
            if val in self.palette_lookup:
                return self.applyOpacity(self.palette_lookup[val])
            if self.colourMap:
                extendedColour = self.getExtendedPaletteColour(val)
                if extendedColour:
                    return extendedColour
        else:
            lwc = self.defaultColour
            lwb = None
            if self.gradients:
                for idx in range(len(self.palette_lookup)):
                    lookup = self.palette_lookup[idx]
                    upb = lookup[0]
                    upc = lookup[1]
                    if val < upb or (idx==len(self.palette_lookup)-1 and val <= upb):
                        if lwb != None:
                            interval = upb - lwb
                            if interval > 0:
                                col = self.computeColour(lwc,upc,(val-lwb)/(upb-lwb))
                                return col
                            else:
                                return lwc
                        else:
                            return self.defaultColour
                    lwb = upb
                    lwc = upc
            else:
                for (val0,val1,col) in self.palette_lookup:
                    if val >= val0 and val < val1:
                        return col
                if val == self.palette_lookup[-1][1]:
                    return self.palette_lookup[-1][2]

            return self.defaultColour

        return self.defaultColour

    def getExtendedPaletteColour(self,discrete_val):
        if self.colourMap in DiscreteColourMaps:
            colours = DiscreteColourMaps[self.colourMap]
            colour = colours[self.colourMapIndex % len(colours)]
            self.colourMapIndex += 1
            self.palette_lookup[discrete_val] = colour
            return colour
        return None

    def drawColourRectangle(self,doc,x,y,width,height,orientation="horizontal",stroke_width=None,stroke=None):
        xc = x
        yc = y

        if orientation=="vertical":
            yc += height

        if self.gradients:
            for idx in range(1,len(self.palette)):
                (val0,col0) = self.palette[idx-1]
                (val1,col1) = self.palette[idx]

                frac = (val1-val0)/(self.maxValue-self.minValue)

                lg = linear_gradient(col0,col1,orientation)
                lgid = lg.getId()
                fill = "url(#"+lgid+")"
                doc.add(lg)

                rw = width
                rh = height
                if orientation=="horizontal":
                    rw = width*frac
                else:
                    rh = height*frac
                    yc = yc - rh
                r = rectangle(xc,yc,rw,rh,stroke=None,stroke_width=0)
                r.addAttr("fill",fill)
                doc.add(r)
                if orientation=="horizontal":
                    xc += rw
        else:
            for (val0,val1,col) in self.palette:
                frac = (val1 - val0) / (self.maxValue - self.minValue)
                rw = width
                rh = height
                if orientation == "horizontal":
                    rw = width * frac
                else:
                    rh = height * frac
                    yc = yc - rh
                r = rectangle(xc, yc, rw, rh, stroke=None, stroke_width=0)
                r.addAttr("fill", col)
                doc.add(r)
                if orientation == "horizontal":
                    xc += rw

        if stroke_width:
            r = rectangle(x,y,width,height,stroke=stroke,stroke_width=stroke_width)
            doc.add(r)



