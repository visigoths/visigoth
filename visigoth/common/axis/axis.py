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


import datetime
from math import pi, log10, ceil

from visigoth.common.diagram_element import DiagramElement
from visigoth.svg import line, text
from visigoth.utils.mapping import Projections
from visigoth.common.axis.axisutils import AxisUtils
from visigoth.utils.fonts.fontmanager import FontManager

class Axis(DiagramElement):

    """
    Construct an axis

    Arguments:
        length(int): length of the axis in pixels
        orientation(str):  horizontal or vertical


    Keyword Arguments:
        minValue(numeric): lower bound for continuous axis
        maxValue(numeric): upper bound for continuous axis
        discreteValues(list): list of values for discrete axis
        projection(visigoth.utils.mapping.projections.Projection): the projection in use
        label(str): label for axis
        labelfn(function): function which accepts an axis value and returns a label string
        stroke(str): stroke colour for axis line
        stroke_width(int): width of axis line
        font_height(int): the axis label font size in pixels 
        axis_font_height(int): the axis value font size in pixels
        text_attributes(dict): a dict containing SVG name/value pairs
    """

    def __init__(self,length,orientation,minValue=None,maxValue=None,discreteValues=None,projection=Projections.IDENTITY,label=None,labelfn=None,stroke="black",stroke_width=2,font_height=24,axis_font_height=16,text_attributes={}):
        DiagramElement.__init__(self)
        self.length = length
        self.orientation = orientation
        self.minValue = minValue
        self.maxValue = maxValue
        self.discreteValues = discreteValues
        self.label = label
        self.labelfn = labelfn
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.font_height = font_height
        self.axis_font_height = axis_font_height
        self.text_attributes = text_attributes
        self.tickpoints = []
        self.ticks = []
        self.axis_utils = None
        self.tick_width = self.stroke_width*2
        self.width = 0
        self.height = 0
        self.projection = projection
        self.integer_ticks = False
        self.integer_interval = None
        self.decimal_places = None

    def setMinValue(self,value):
        self.minValue = value
        return self

    def getMinValue(self):
        return self.minValue

    def setLength(self,length):
        self.length = length
        return self

    def setMaxValue(self,value):
        self.maxValue = value
        return self

    def getMaxValue(self):
        return self.maxValue
        
    def setLabel(self,label):
        self.label = label
        return self

    def setDecimalPlaces(self,decimal_places):
        self.decimal_places = decimal_places

    def extractBounds(self,lwb,upb):
        lwb_date = isinstance(lwb,datetime.datetime)
        upb_date = isinstance(upb,datetime.datetime)
        if lwb_date and upb_date:
            return (lwb.timestamp(),upb.timestamp(),True)
        else:
            if lwb_date or upb_date:
                raise Exception("both lwb and upb should be date")
            return (float(lwb),float(upb),False)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def setFontHeight(self,font_height):
        self.axis_font_height = font_height
        return self

    def setLabelFontHeight(self,font_height):
        self.font_height = font_height
        return self

    def setTextAttributes(self,text_attributes):
        self.text_attributes = text_attributes
        return self

    def setIntegerTicks(self,interval=1):
        self.integer_ticks = True
        self.integer_interval = interval

    def setStroke(self,stroke,stroke_width):
        """
        Configure line colour and width

        Arguments:
           stroke(str): stroke colour for axis line
           stroke_width(int): width of axis line
        """
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.tick_width = self.stroke_width * 2
        return self

    def setTickPositions(self,tickpositions):
        self.tickpoints = tickpositions
        return self

    def getTickPositions(self,start):
        return self.axisutils.getTickPositions(start)

    def getPointPosition(self,start,value):
        if self.discreteValues:
            if value in self.discreteValues:
                tickwidth = self.length / len(self.discreteValues)
                i = self.discreteValues.index(value)
                return start + tickwidth*(i + 0.5)
            else:
                return None
        return self.axisutils.getPointPosition(start,value)

    def isDiscrete(self):
        return self.discreteValues is not None

    def build(self,fmt):
        if self.discreteValues:
            self.tickpoints = self.discreteValues
            self.ticks = [(value, value) for value in self.tickpoints]
            self.axisutils = None
        else:
            (self.lwb,self.upb,self.date_based) = self.extractBounds(self.minValue,self.maxValue)
            self.axisutils = AxisUtils(self.length,self.orientation,self.lwb,self.upb,self.projection,self.date_based)
            if self.integer_ticks:
                self.axisutils.setIntegerInterval(self.integer_interval)

            if not self.tickpoints:
                self.tickpoints = self.axisutils.computeTickPoints()
            else:
                self.axisutils.setTickPoints(self.tickpoints[:])

            if not self.labelfn:
                if self.date_based:
                    self.labelfn = lambda val:str(val)
                else:
                    spacing = self.axisutils.getSpacing()
                    l10s = log10(spacing)
                    if spacing == float(int(spacing)):
                        if l10s > 5:
                            self.axis_format = "%.2e"
                        else:
                            self.axis_format = "%.0f"
                    else:
                        if l10s < -5:
                            self.axis_format = "%.2e"
                        else:
                            if self.decimal_places is None:
                                self.decimal_places = max(2,2-round(log10(self.maxValue - self.minValue)))
                            axis_dp = self.decimal_places
                            if axis_dp < 0:
                                axis_dp = ceil(abs(l10s))
                            self.axis_format = "%."+str(axis_dp)+"f"

                    self.labelfn = lambda v: self.axis_format%(v)

            self.ticks = [(point,self.labelfn(point)) for point in self.tickpoints]

        maxlen = max([FontManager.getTextLength(self.text_attributes,label,self.axis_font_height) for (tickv,label) in self.ticks])

        self.width = self.length
        self.height = self.stroke_width+maxlen
        if self.label:
            self.height += 2*self.font_height
        if self.orientation == "vertical":
            oldh = self.height
            self.height = self.width
            self.width = oldh

    def draw(self,doc,cx,cy):

        ox = cx - self.width/2
        oy = cy - self.height/2

        oo = ox if self.orientation == "horizontal" else oy
        if self.discreteValues:
            tickwidth = self.length / len(self.discreteValues)
            positions = [oo + (i + 0.5) * tickwidth for i in range(len(self.discreteValues))]
        else:
            positions = self.axisutils.getTickPositions(oo)

        if self.orientation == "horizontal":
            l = line(ox,oy,ox+self.width,oy,self.stroke,self.stroke_width)
            l.addAttr("stroke-linecap","square")
            doc.add(l)

            if self.label:
                t = text(cx,oy+self.height-self.font_height,self.label)
                t.addAttr("font-size",self.font_height)
                t.setVerticalCenter()
                doc.add(t)

            for idx in range(len(self.ticks)):
                (tv,label) = self.ticks[idx]
                tx = positions[idx]
                tl = line(tx,oy,tx,oy+self.tick_width,self.stroke,self.stroke_width)
                tt = text(tx+self.axis_font_height/2,oy+self.tick_width,label)
                tt.setRotation(pi/-2)
                tt.addAttr("font-size",self.axis_font_height)
                tt.addAttr("text-anchor", "end")
                doc.add(tl)
                doc.add(tt)

        else:
            l = line(ox+self.width,oy,ox+self.width,oy+self.height,self.stroke,self.stroke_width)
            l.addAttr("stroke-linecap","square")
            doc.add(l)

            if self.label:
                t = text(ox+self.font_height,cy-self.font_height/2,self.label)
                t.addAttr("font-size",self.font_height)
                t.setRotation(pi/-2)
                doc.add(t)

            for idx in range(len(self.ticks)):
                (tv,label) = self.ticks[idx]
                ty = positions[idx]
                tl = line(ox+self.width,ty,ox+self.width-self.tick_width,ty,self.stroke,self.stroke_width)
                tt = text(ox+self.width-self.tick_width,ty+self.axis_font_height/2,label)
                tt.addAttr("text-anchor", "end")
                tt.addAttr("font-size",self.axis_font_height)
                doc.add(tl)
                doc.add(tt)
