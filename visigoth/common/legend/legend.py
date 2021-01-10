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

import os.path

from visigoth.svg import text, polygon, circle, line
from visigoth.common.diagram_element import DiagramElement
from visigoth.common.axis import Axis
from visigoth.utils.js import Js
from visigoth.utils.fonts.fontmanager import FontManager
from visigoth.utils.colour import ContinuousColourManager

class Legend(DiagramElement):
    """
    Create a legend graphic describing the colours used in a colour_manager

    Arguments:
        colour_manager(visigoth.utils.colour.Palette): a colour_manager object

    Keyword Arguments:
        width(int): width of the legend area
        label(str): a descriptive label to display
        labelfn(function): function which accepts an axis value and returns a label string
        orientation(str): "horizontal"|"vertical" whether to display legend horizontally or vertically (applies only to continuous colour_manager)
        legend_columns(int): the number of columns to split the legend into (applies only to discrete colour_manager)
        stroke(str): the stroke colour for the line around the toggle control
        stroke_width(int): the stroke width for the line around the toggle control
        font_height(int): the font size for the legend (optional, defaults to 24)
        text_attributes(dict): a dict containing SVG name/value pairs
    """

    def __init__(self,colour_manager,width=512,label=None,labelfn=None,orientation="horizontal",legend_columns=0,stroke="black",stroke_width=2, font_height=24,text_attributes={}):
        DiagramElement.__init__(self)
        self.colour_manager = colour_manager
        self.text_attributes = text_attributes
        self.width = width
        self.height = 0
        self.axis = None
        self.label = label
        self.labelfn = labelfn
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.font_height = font_height

        # Discrete
        self.legend_gap = 20
        self.legend_columns = legend_columns

        self.discrete_marker_style = "square"

        # Continuous
        self.orientation = orientation

        if isinstance(self.colour_manager,ContinuousColourManager):
            self.configureForContinuousColourManager()
            self.axis = Axis(self.width-2*self.colour_manager.getCapSize(), self.orientation, self.colour_manager.getMinValue(), self.colour_manager.getMaxValue(),
                         label=self.label, labelfn=self.labelfn, font_height=self.font_height, axis_font_height=self.font_height, text_attributes=self.text_attributes,
                         stroke=self.stroke, stroke_width=self.stroke_width)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def getAxis(self):
        return self.axis

    def setDiscreteMarkerStyle(self,style):
        self.discrete_marker_style = style

    def configureForContinuousColourManager(self,bar_thickness=40,bar_spacing=10):
        """
        Configure the legend for displaying a continuous colour_manager

        Arguments:
            bar_thickness(integer): the thickness of the bar in pixels
            bar_spacing(integer): the spacing between the bar and the labels
        Returns:
            self
        """
        self.bar_width = bar_thickness
        self.bar_spacing = bar_spacing
        return self

    def build(self,fmt):
        self.colour_manager.build()
        if self.colour_manager.isDiscrete():
            if not self.legend_columns:
                max_text_width = max(map(lambda x:FontManager.getTextLength(self.text_attributes,self.colour_manager.getLabel(x[0]),self.font_height),self.colour_manager.getCategories()))
                column_content_width = max_text_width + self.font_height*3
                self.legend_columns = max(1,self.width // column_content_width)
            self.height = (self.font_height*len(self.colour_manager.getCategories())*2) // self.legend_columns
        else:
            self.axis.setMinValue(self.colour_manager.getMinValue())
            self.axis.setMaxValue(self.colour_manager.getMaxValue())
            tickpoints = self.colour_manager.getTickPositions()
            self.axis.setTickPositions(tickpoints)
            self.axis.build(fmt)
            if self.orientation == "horizontal":
                self.height = self.bar_width + self.bar_spacing + self.axis.getHeight()
            else:
                self.height = self.width
                self.width = self.bar_width + self.bar_spacing + self.axis.getWidth()

    def draw(self,d,cx,cy):
        if self.colour_manager.isDiscrete():
            config = self.drawDiscrete(d,cx,cy)
        else:
            config = self.drawContinuous(d,cx,cy)

        with open(os.path.join(os.path.split(__file__)[0],"legend.js"),"r") as jsfile:
            jscode = jsfile.read()
        Js.registerJs(d,self,jscode,"legend",cx,cy,config)

    def drawDiscrete(self,d,cx,cy):
        oy = cy - self.height/2
        ox = cx
        legend_column_width = self.width / self.legend_columns
        max_text_width = max(map(lambda x:FontManager.getTextLength(self.text_attributes,str(x[0]),self.font_height),self.colour_manager.getCategories()))
        column_content_width = max_text_width + self.font_height*1.5
        column_offset = 0
        if column_content_width < legend_column_width:
            column_offset = (legend_column_width-column_content_width)/2
        legend_y = oy
        legend_x = ox - (self.width/2) + column_offset
        col = 0
        config = { "categories": {} }
        for (category, colour) in self.colour_manager.getCategories():
            label = self.colour_manager.getLabel(category)
            g = self.font_height
            if self.discrete_marker_style == "square":
                points = [(legend_x, legend_y), (legend_x + g, legend_y), (legend_x + g, legend_y + g),
                      (legend_x, legend_y + g)]
                p = polygon(points, colour, self.stroke, self.stroke_width)
            elif self.discrete_marker_style == "circle":
                p = circle(legend_x+g/2,legend_y+g/2,g/2,fill=colour,stroke=self.stroke,stroke_width=self.stroke_width)
            else:
                p = line(legend_x,legend_y+g/2,legend_x+g,legend_y+g/2,stroke=colour,stroke_width=self.stroke_width)
            config["categories"][category] = [p.getId()];
            d.add(p)
            t = text(legend_x+1.5*g, legend_y+g/2, label)
            t.addAttr("font-size", self.font_height)
            t.addAttr("text-anchor", "start")
            t.setVerticalCenter()
            t.addAttrs(self.text_attributes)
            d.add(t)
            col += 1
            if col >= self.legend_columns:
                legend_y += 2 * g
                legend_x = ox - (self.width/2) + column_offset
                col = 0
            else:
                legend_x += legend_column_width

        return config

    def drawContinuous(self,d,cx,cy):
        ox = cx - self.getWidth()/2
        oy = cy - self.getHeight()/2
        if self.orientation == "horizontal":
            self.axis.draw(d,cx,oy+self.bar_width+self.bar_spacing+self.axis.getHeight()/2)
            self.colour_manager.drawColourRectangle(d,ox,oy,self.getWidth(),self.bar_width,self.orientation,stroke=self.stroke,stroke_width=self.stroke_width)
        else:
            self.axis.draw(d,ox+self.axis.getWidth()/2,cy)
            self.colour_manager.drawColourRectangle(d,ox+self.axis.getWidth(),oy,self.bar_width,self.getHeight(),self.orientation,stroke=self.stroke,stroke_width=self.stroke_width)
        return {}