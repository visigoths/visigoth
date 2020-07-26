# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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
from visigoth.map_layers.geoimport import Geoimport
from visigoth.utils.js import Js
from visigoth.utils.colour import ContinuousPalette


class Chloropleth(Geoimport):

    """
    Create a Choloropleth plot from a geojson file

    Arguments:
        path(str) : file path to a geojson file
        valueNameOrFn(str|function) : the name of the property (or function of the properties dict) to provide the value to visualize

    Keyword Arguments:
        labelNameOrFn(str|function) : the name of the property (or function of the properties dict) to provide the label
        palette(DiscretePalette|ContinuousPalette) : a DiscretePalette|ContinuousPalette object for mapping values to colours
        stroke (str): stroke color
        stroke_width (int): stroke width

    Notes:

    """

    def __init__(self, path, valueNameOrFn, labelNameOrFn=None, palette=None, stroke="black",stroke_width=2):
        super().__init__(path,polygon_style=lambda props:self.getPolygonStyle(props))
        self.path = path
        self.valueNameOrFn = valueNameOrFn
        self.labelNameOrFn = labelNameOrFn
        self.stroke = stroke
        if palette is None:
            palette = ContinuousPalette()
        self.setPalette(palette)
        self.stroke_width = stroke_width
        for props in self.getPolygonProperties():
            col = self.getPalette().getColour(self.valueNameOrFn(props))

    def getFill(self,geojson_props):
        if isinstance(self.valueNameOrFn,str):
            if self.valueNameOrFn in geojson_props:
                val = geojson_props[self.valueNameOrFn]
            else:
                return self.getPalette().getDefaultColour()
        else:
            val = self.valueNameOrFn(geojson_props)
        return self.getPalette().getColour(val)

    def getLabel(self,geojson_props):
        if self.labelNameOrFn in geojson_props:
            return geojson_props[self.labelNameOrFn]
        return ""

    def getPolygonStyle(self,geojson_props):
        return {
            "fill": self.getFill(geojson_props),
            "tooltip": self.getLabel(geojson_props),
            "label": self.getLabel(geojson_props),
            "stroke": self.stroke,
            "stroke_width": self.stroke_width
        }

    def draw(self,doc,cx,cy):
        config = super().draw(doc,cx,cy,False)
        with open(os.path.join(os.path.split(__file__)[0],"chloropleth.js"),"r") as jsfile:
            jscode = jsfile.read()
        Js.registerJs(doc,self,jscode,"chloropleth",cx,cy,config)
