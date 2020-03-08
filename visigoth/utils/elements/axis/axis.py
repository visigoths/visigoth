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


import json
import datetime
from math import pi, floor, log10, ceil

from visigoth.common.diagram_element import DiagramElement
from visigoth.svg import line, text
from visigoth.utils.mapping import Projections
from visigoth.utils.elements.axis.axisutils import AxisUtils
from visigoth.utils.fonts.fontmanager import FontManager

class Axis(DiagramElement):

    """
    Construct an axis

    Arguments:
        length(int): length of the axis in pixels
        orientation(str):  horizontal or vertical
        minValue(numeric): lower bound for axis 
        maxValue(numeric): upper bound for axis 

    Keyword Arguments:
        projection(visigoth.utils.mapping.projections.Projection): the projection in use
        label(str): label for axis
        decimal_places(int): the number of decimal places to display
        labelfn(function): function which accepts an axis value and returns a label string (overrides decimal_places)
        stroke(str): stroke colour for axis line
        stroke_width(int): width of axis line
        font_height(int): the axis label font size in pixels 
        axis_font_height(int): the axis value font size in pixels
        text_attributes(dict): a dict containing SVG name/value pairs
    """

    def __init__(self,length,orientation,minValue,maxValue,projection=Projections.IDENTITY,label=None,decimal_places=2,labelfn=None,stroke="black",stroke_width=2,font_height=24,axis_font_height=16,text_attributes={}):
        DiagramElement.__init__(self)
        self.length = length
        self.orientation = orientation
        self.minValue = minValue
        self.maxValue = maxValue
        self.label = label
        self.labelfn = labelfn
        self.decimal_places = decimal_places
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

    def setMinValue(self,value):
        self.minValue = value

    def getMinValue(self):
        return self.minValue

    def setLength(self,length):
        self.length = length

    def setMaxValue(self,value):
        self.maxValue = value

    def getMaxValue(self):
        return self.maxValue
        
    def setLabel(self,label):
        self.label = label

    def extractBounds(self,lwb,upb):
        date_based = False
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

    def setStroke(self,stroke,stroke_width):
        """
        Configure line colour and width

        Arguments:
           stroke(str): stroke colour for axis line
           stroke_width(int): width of axis line
        """
        self.stroke = stroke
        self.stroke_width = stroke_width

    def getTickPoints(self):
        return self.tickpoints

    def setTickPositions(self,tickpositions):
        self.tickpoints = tickpositions

    def getTickPositions(self,start):
        return self.axisutils.getTickPositions(start)

    def getPointPosition(self,start,value):
        return self.axisutils.getPointPosition(start,value)

    def build(self):
        (self.lwb,self.upb,self.date_based) = self.extractBounds(self.minValue,self.maxValue)
        self.axisutils = AxisUtils(self.length,self.orientation,self.lwb,self.upb,self.projection,self.date_based)
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

        if self.orientation == "horizontal":
            l = line(ox,oy,ox+self.width,oy,self.stroke,self.stroke_width)
            l.addAttr("stroke-linecap","square")
            doc.add(l)

            if self.label:
                t = text(cx,oy+self.height-self.font_height,self.label)
                t.addAttr("font-size",self.font_height)
                t.setVerticalCenter()
                doc.add(t)

            positions = self.axisutils.getTickPositions(ox)
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

            positions = self.axisutils.getTickPositions(oy)
            for idx in range(len(self.ticks)):
                (tv,label) = self.ticks[idx]
                ty = positions[idx]
                tl = line(ox+self.width,ty,ox+self.width-self.tick_width,ty,self.stroke,self.stroke_width)
                tt = text(ox+self.width-self.tick_width,ty+self.axis_font_height/2,label)
                tt.addAttr("text-anchor", "end")
                tt.addAttr("font-size",self.axis_font_height)
                doc.add(tl)
                doc.add(tt)
