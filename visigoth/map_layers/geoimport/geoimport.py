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

import random
import sys
import json
import copy
import os.path
from math import radians,sin,cos,pi,sqrt,log
import logging

from visigoth.svg import polygon, circle, path, line, rectangle, clip_path
from visigoth.map_layers import MapLayer
from visigoth.map_layers.geoplot import Geoplot,Multipoint,Multiline,Multipolygon

from visigoth.containers.box import Box
from visigoth.utils.mapping import Mapping
from visigoth.utils.geojson import GeojsonReader
from visigoth.utils.geopackage import GeopackageReader
from visigoth.utils.js import Js

class Geoimport(MapLayer):

    """
    Import and plot a layer composed of points, lines and polygons described in a source file
    source file formats supported are geojson (.geojson) or geopackage (.gpkg) (experimental)
    tiles are currently not imported from geopackage files

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
        super(Geoimport, self).__init__()
        self.path = path
        self.width = None
        self.height = None
        self.point_style = point_style
        self.line_style = line_style
        self.polygon_style = polygon_style
        self.multipolys = []
        self.multipoints = []
        self.multilines = []
        self.boundaries = None
        self.projection = None
        self.geoplot = None
        self.extracted = False

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
        self.width = width
        self.height = height
        self.ownermap = ownermap
        self.boundaries = boundaries
        self.projection = projection
        self.zoom_to = zoom_to

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

    def getWidth(self):
        return self.geoplot.getWidth()

    def getHeight(self):
        return self.geoplot.getHeight()

    def extractGeojson(self):
        reader = GeojsonReader()
        return reader.extract(self.path)

    def extractGeopackage(self):
        reader = GeopackageReader()
        return reader.extract(self.path)

    def trackBoundaries(self,point):
        (lon,lat) = point
        if self.min_lon == None or lon < self.min_lon:
            self.min_lon = lon
        if self.min_lat == None or lat < self.min_lat:
            self.min_lat = lat
        if self.max_lon == None or lon > self.max_lon:
            self.max_lon = lon
        if self.max_lat == None or lat > self.max_lat:
            self.max_lat = lat

    def getBoundaries(self):
        self.extract()

        self.min_lat = None
        self.min_lon = None
        self.max_lat = None
        self.max_lon = None

        for (_,points) in self.multipoints:
            for point in points:
                self.trackBoundaries(point)
        for (_,lines) in self.multilines:
            for line in lines:
                for point in line:
                    self.trackBoundaries(point)
        for (_,polys) in self.multipolys:
            for poly in polys:
                for ring in poly:
                    for point in ring:
                        self.trackBoundaries(point)

        return ((self.min_lon,self.min_lat),(self.max_lon,self.max_lat))

    def extract(self):
        if self.extracted:
            return
        self.extracted = True

        fext = os.path.splitext(self.path)[1]
        if fext == ".geojson":
            (gpoints,glines,gpolys) = self.extractGeojson()
        elif fext == ".gpkg":
            (gpoints,glines,gpolys) = self.extractGeopackage()
        else:
            msg = "Unable to import file with extension %s"%(fext)
            logging.getLogger("Geofile").error(msg)
            raise Exception(msg)

        self.multipoints = gpoints
        self.multilines = glines
        self.multipolys = gpolys

    def build(self):
        self.extract()
        multipoints = []
        for (props,points) in self.multipoints:
            multipoints.append(Multipoint(points,**self.getPointStyle(props)))

        multilines = []
        for (props,lines) in self.multilines:
            multilines.append(Multiline(lines,**self.getLineStyle(props)))

        multipolys = []
        for (props,polys) in self.multipolys:
            multipolys.append(Multipolygon(polys,**self.getPolygonStyle(props)))

        self.geoplot = Geoplot(multilines=multilines,multipoints=multipoints,multipolys=multipolys)
        self.geoplot.configureLayer(self.ownermap,self.width,self.height,self.boundaries,self.projection,self.zoom_to)
        self.geoplot.build()

    def draw(self,doc,cx,cy):
        self.geoplot.draw(doc,cx,cy)
        with open(os.path.join(os.path.split(__file__)[0],"geoimport.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc,self,jscode,"geoimport",cx,cy,config)
        doc.getDiagram().connect(self,"zoom",self.geoplot,"zoom")
        doc.getDiagram().connect(self,"visible_window",self.geoplot,"visible_window")