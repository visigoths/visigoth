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
import logging

from visigoth.map_layers.geoplot import Geoplot,Multipoint,Multiline,Multipolygon

from visigoth.utils.geojson import GeojsonReader
from visigoth.utils.js import Js

class Geoimport(Geoplot):

    """
    Import and plot a layer composed of points, lines and polygons described in a source file
    source file formats supported are geojson (.geojson)

    Arguments:
        path: path to the file to be imported

    Keyword Arguments:
        path (str): path to file to import
        point_style (dict|function): see Notes
        line_style (dict|function): see Notes
        polygon_style (dict|function): see Notes
        
    Notes:
        The point_style, line_style and polygon_style values should be dicts or functions operating on a properties dict and returning a style dict
        The returned dict describes the SVG rendering style for the element (point, line, area)
        Possible keys are "label", tooltip", "fill", "stroke", "stroke_width", "radius", "popup" and "marker"
        These keys map to keyword arguments of the geoplot.Multipoint, geoplot.Multiline and geoplot.Multipolygon instances
    """

    def __init__(self, path, point_style=lambda p:{}, line_style=lambda p:{}, polygon_style=lambda p:{}):
        super().__init__()
        self.path = path
        self.point_style = point_style
        self.line_style = line_style
        self.polygon_style = polygon_style
        self.objects = self.extract()

    def getPointStyle(self,props):
       return self.invoke(self.point_style,[props])

    def getLineStyle(self,props):
       return self.invoke(self.line_style,[props])

    def getPolygonStyle(self,props):
       return self.invoke(self.polygon_style,[props])

    def invoke(self,fn_or_val,args):
        if fn_or_val and fn_or_val.__class__.__name__ == "function":
            return fn_or_val(*args)
        else:
            return fn_or_val

    def extractGeojson(self):
        reader = GeojsonReader()
        return reader.extract(self.path)

    def extract(self):
        (points,lines,polys) = self.extractGeojson()

        # register the points/lines and polys without style information
        # so the boundaries are established.  Re-add them during build.
        for (_, ppoints) in points:
            self.add(Multipoint(points))

        for (_, plines) in lines:
            self.add(Multiline(plines))

        for (_, ppolys) in polys:
            self.add(Multipolygon(ppolys))

        return (points,lines,polys)

    def getPolygonProperties(self):
        (opoints, olines, opolys) = self.objects
        return [props for (props, polys) in opolys]

    def build(self,fmt):
        super().build(fmt)
        self.clear()
        (opoints, olines, opolys) = self.objects

        for (props, points) in opoints:
            self.add(Multipoint(points, **self.getPointStyle(props)))

        for (props, lines) in olines:
            self.add(Multiline(lines, **self.getLineStyle(props)))

        for (props, polys) in opolys:
            self.add(Multipolygon(polys, **self.getPolygonStyle(props)))


    def draw(self,doc,cx,cy,constructJs=True):
        config = super().draw(doc,cx,cy,False)
        with open(os.path.join(os.path.split(__file__)[0],"geoimport.js"),"r") as jsfile:
            jscode = jsfile.read()
        Js.registerJs(doc,self,jscode,"geoimport",cx,cy,config,constructJs)
        return config