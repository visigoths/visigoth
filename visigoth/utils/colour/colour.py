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

import random
from visigoth.svg import rectangle, linear_gradient
from visigoth.utils.colour.webcolours import colours
from visigoth.utils.colour.colourmaps import DiscreteColourMaps

class ColourException(Exception):

    def __init__(self,msg):
        super().__init__(msg)

class Colour(object):

    webColours = { col["name"].lower():"#"+col["hex"] for col in colours }

    def __init__(self,colour_manager,minValue=None,maxValue=None,defaultColour="red"):
        self.colour_manager = colour_manager
        self.defaultColour = defaultColour
        self.colour_manager_lookup = {}
        if len(self.colour_manager):
            if len(self.colour_manager[0]) == 2:
                # colour_manager is continuous and a list of (val,col) pairs
                self.colour_manager_lookup = []
                for i in range(1,len(self.colour_manager)):
                    (val0,col0) = self.colour_manager[i-1]
                    (val1,col1) = self.colour_manager[i]
                    self.colour_manager_lookup.append((val0, val1, Colour.parseColour(col0), Colour.parseColour(col1)))
                self.gradients = True
            else:
                # colour_manager is continuous and a list of (val1,val2,col) triples
                self.gradients = False
                self.colour_manager_lookup = [(val0, val1, Colour.parseColour(col)) for (val0, val1, col) in self.colour_manager]
        self.opacity = 1.0
        self.minValue = minValue
        self.maxValue = maxValue

    def getOpacity(self):
        return self.opacity

    def setOpacity(self,opacity):
        self.opacity = opacity

    def isDiscrete(self):
        return self.discrete

    @staticmethod
    def parseColour(col):
        if not isinstance(col,str):
            raise ColourException("Unable to parse colour from non-string (%s)" % (str(col)))
        if col and (len(col) != 7 or col[0] != "#"):
            if col.lower() in Colour.webColours:
                col = Colour.webColours[col.lower()]
        if not col or col[0] != "#" or (len(col) != 7 and len(col) != 9):
            raise ColourException("Unable to parse colour (%s)"%(col))
        r = int(col[1:3],16)
        g = int(col[3:5],16)
        b = int(col[5:7],16)
        a = 255 if len(col) == 7 else int(col[7:9],16)
        return (r,g,b,a)

    def computeColour(self,col1,col2,frac):
        r = col1[0]+int(frac*(col2[0]-col1[0]))
        g = col1[1]+int(frac*(col2[1]-col1[1]))
        b = col1[2]+int(frac*(col2[2]-col1[2]))
        a = col1[3] + int(frac * (col2[3] - col1[3]))
        return self.rgb2colour((r,g,b,a))

    @staticmethod
    def toHEX(colour):
        if colour is None:
            return None
        return Colour.rgb2colour(Colour.parseColour(colour))
    
    @staticmethod
    def rgb2colour(rgba):
        (r,g,b,a) = rgba
        return "#%02X%02X%02X%02X" % (r, g, b, a)

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

    @staticmethod
    def applyOpacity(colour,opacity):
        if opacity < 1.0:
            (r,g,b,a) = Colour.parseColour(colour)
            return "#%02X%02X%02X%02X"%(r,g,b,round(opacity*255))
        else:
            return colour

    def getColour(self,val):
        if self.gradients:
            for idx in range(len(self.colour_manager_lookup)):
                lookup = self.colour_manager_lookup[idx]
                (lwb,upb,lwc,upc) = lookup
                if val >= lwb and (val < upb or (idx==len(self.colour_manager_lookup)-1 and val <= upb)):
                    col = self.computeColour(lwc,upc,(val-lwb)/(upb-lwb))
                    return col
        else:
            for (val0,val1,col) in self.colour_manager_lookup:
                if val >= val0 and val < val1:
                    return self.rgb2colour(col)
            if val == self.colour_manager_lookup[-1][1]:
                return self.rgb2colour(self.colour_manager_lookup[-1][2])

        return self.defaultColour


    def drawColourRectangle(self,doc,x,y,width,height,orientation="horizontal",stroke_width=None,stroke=None):
        xc = x
        yc = y

        # add a half pixel shim to the width or height of each colour band depending on orientation
        # this avoids narrow "gaps" between colour bands when rendered in some browsers
        w_shim = 0
        h_shim = 0

        if orientation=="vertical":
            yc += height
            h_shim = 0.5
        else:
            w_shim = 0.5

        if self.gradients:
            for idx in range(1,len(self.colour_manager)):
                (val0,col0) = self.colour_manager[idx-1]
                (val1,col1) = self.colour_manager[idx]

                frac = (val1-val0)/(self.maxValue-self.minValue)
                rw = width
                rh = height

                if orientation=="horizontal":
                    rw = width*frac
                    th = rw
                else:
                    rh = height*frac
                    yc = yc - rh
                    th = rh

                if th < 5:
                    # if there are a lot of narrow colour bands (< 5 pixels)
                    # just use a solid colour block with the mid point colour instead of a linear gradient
                    fill = self.computeColour(Colour.parseColour(col0),Colour.parseColour(col1),0.5)
                else:
                    lg = linear_gradient(col0,col1,orientation)
                    lgid = lg.getId()
                    fill = "url(#"+lgid+")"
                    doc.add(lg)

                r = rectangle(xc,yc,rw+w_shim,rh+h_shim,stroke=None,stroke_width=0)
                r.addAttr("fill",fill)
                doc.add(r)
                if orientation=="horizontal":
                    xc += rw
        else:
            for (val0,val1,col) in self.colour_manager:
                frac = (val1 - val0) / (self.maxValue - self.minValue)
                rw = width
                rh = height
                if orientation == "horizontal":
                    rw = width * frac
                else:
                    rh = height * frac
                    yc = yc - rh
                r = rectangle(xc, yc, rw+w_shim, rh+h_shim, stroke=None, stroke_width=0)
                r.addAttr("fill", col)
                doc.add(r)
                if orientation == "horizontal":
                    xc += rw

        if stroke_width:
            r = rectangle(x,y,width,height,stroke=stroke,stroke_width=stroke_width)
            doc.add(r)



