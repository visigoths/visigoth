# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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
from visigoth.map_layers.geoimport import Geoimport
from visigoth.utils.js import Js
from visigoth.utils.colour import ContinuousPalette


class Chloropleth(Geoimport):

    """
    Create a Choloropleth plot from a geojson file

    Arguments:
        path : file path to a geojson file
        valueNameOrFn(str|function) : the name of the property (or function of the properties dict) to provide the value to visualize
        labelNameOrFn(str|function) : the name of the property (or function of the properties dict) to provide the label
        palette(list) : a DiscretePalette|ContinuousPalette object for mapping values to colours

    Keyword Arguments:
        stroke (str): stroke color
        stroke_width (int): stroke width

    Notes:

    """

    def __init__(self, path, valueNameOrFn, labelNameOrFn, palette, stroke="black",stroke_width=2):
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
            self.getPalette().getColour(self.valueNameOrFn(props))

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
