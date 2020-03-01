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

import os.path

from visigoth.svg import text, polygon
from visigoth.common.diagram_element import DiagramElement
from visigoth.utils.elements.axis import Axis
from visigoth.utils.colour import Colour
from visigoth.utils.js import Js
from visigoth.utils.fonts.fontmanager import FontManager

class Legend(DiagramElement):
    """
    Create a legend graphic describing the colours used in a palette

    Arguments:
        palette(visigoth.utils.colour.Palette): a palette object

    Keyword Arguments:
        width(int): width of the legend area
        label(str): a descriptive label to display
        orientation(str): "horizontal"|"vertical" whether to display legend horizontally or vertically (continuous palette)
        legend_columns(int): the number of columns to split the legend into
        stroke(str): the stroke colour for the line around the toggle control
        stroke_width(int): the stroke width for the line around the toggle control
        font_height(int): the font size for the legend (optional, defaults to 24)
        text_attributes(dict): a dict containing SVG name/value pairs
        decimal_places(int): the number of decimal places to display
    """

    def __init__(self,palette,width=512,label=None,orientation="horizontal",legend_columns=0,stroke="black",stroke_width=2, font_height=24,text_attributes={},decimal_places=3):
        DiagramElement.__init__(self)
        self.palette = palette
        self.text_attributes = text_attributes
        self.width = width
        self.height = 0
        self.axis = None
        self.label = label
        self.stroke = stroke
        self.stroke_width = stroke_width

        # Discrete
        self.legend_gap = 20
        self.legend_columns = legend_columns
        self.legend_font_height = font_height

        # Continuous
        self.orientation = orientation
        self.decimal_places = decimal_places
        self.bar_width = 40 # width of legend bar
        self.bar_spacing = 10 # space between axis and legend bar

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def build(self):
        if self.palette.isDiscrete():
            if not self.legend_columns:
                max_text_width = max(map(lambda x:FontManager.getTextLength(self.text_attributes,x[0],self.legend_font_height),self.palette.getCategories()))
                column_content_width = max_text_width + self.legend_font_height*3
                self.legend_columns = max(1,self.width // column_content_width)
            self.height = (self.legend_font_height*len(self.palette.getCategories())*2) // self.legend_columns
        else:
            self.axis = Axis(self.width,self.orientation,self.palette.getMinValue(),self.palette.getMaxValue(),label=self.label,font_height=self.legend_font_height,text_attributes=self.text_attributes,stroke=self.stroke,stroke_width=self.stroke_width,decimal_places=self.decimal_places)
            self.axis.build()
            if self.orientation == "horizontal":
                self.height = self.bar_width + self.bar_spacing + self.axis.getHeight()
                self.width = self.axis.getWidth()
            else:
                self.height = self.axis.getHeight()
                self.width = self.bar_width + self.bar_spacing + self.axis.getWidth()

    def draw(self,d,cx,cy):
        if self.palette.isDiscrete():
            config = self.drawDiscrete(d,cx,cy)
        else:
            # rebuild the axis in case a continuous palette has been rescaled
            self.axis = Axis(self.width,self.orientation,self.palette.getMinValue(),self.palette.getMaxValue(),label=self.label,font_height=self.legend_font_height,text_attributes=self.text_attributes,stroke=self.stroke,stroke_width=self.stroke_width,decimal_places=self.decimal_places)
            self.axis.build()

            config = self.drawContinuous(d,cx,cy)

        with open(os.path.join(os.path.split(__file__)[0],"legend.js"),"r") as jsfile:
            jscode = jsfile.read()
        Js.registerJs(d,self,jscode,"legend",cx,cy,config)

    def drawDiscrete(self,d,cx,cy):
        oy = cy - self.height/2
        ox = cx
        legend_column_width = self.width / self.legend_columns
        max_text_width = max(map(lambda x:FontManager.getTextLength(self.text_attributes,x[0],self.legend_font_height),self.palette.getCategories()))
        column_content_width = max_text_width + self.legend_font_height*1.5
        column_offset = 0
        if column_content_width < legend_column_width:
            column_offset = (legend_column_width-column_content_width)/2
        legend_y = oy
        legend_x = ox - (self.width/2) + column_offset
        col = 0
        config = { "categories": {} }
        for (category, colour) in self.palette.getCategories():
            g = self.legend_font_height
            points = [(legend_x, legend_y), (legend_x + g, legend_y), (legend_x + g, legend_y + g),
                      (legend_x, legend_y + g)]
            p = polygon(points, colour, self.stroke, self.stroke_width)
            config["categories"][category] = [p.getId()];
            d.add(p)
            t = text(legend_x+1.5*g, legend_y+g/2, category)
            t.addAttr("font-size", self.legend_font_height)
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
            self.palette.drawColourRectangle(d,ox,oy,self.getWidth(),self.bar_width,self.orientation,stroke=self.stroke,stroke_width=self.stroke_width)
        else:
            self.axis.draw(d,ox+self.axis.getWidth()/2,cy)
            self.palette.drawColourRectangle(d,ox+self.axis.getWidth(),oy,self.bar_width,self.getHeight(),self.orientation,stroke=self.stroke,stroke_width=self.stroke_width)
        return {}