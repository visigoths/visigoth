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

import json
import logging

class GeojsonReader(object):

    """
    Create a Geojson reader

    """

    def __init__(self):
        super(GeojsonReader, self).__init__()

    def extract(self,path):
        with open(path) as f:
            data = json.loads(f.read())
        self.points = []
        self.lines = []
        self.polys = []
        gt = data["type"]
        if gt == "FeatureCollection":
            for feature in data["features"]:
                self.processFeature(feature)
        if gt == "Feature":
            props = {}
            if "properties" in data:
                props = data["properties"]
            geometry = data["geometry"]
            self.processGeometry(geometry,props)
        return (self.points,self.lines,self.polys)

    def processFeature(self,data):
        gt = data["type"]
        if gt == "Feature":
            props = {}
            if "properties" in data:
                props = data["properties"]
            geometry = data["geometry"]
            self.processGeometry(geometry,props)
        else:
            logging.getLogger("GeojsonReader").warning("Unable to process geojson data of type=%s"%(gt))

    def processGeometry(self,geometry,props):
        gtype = geometry["type"]
        if gtype == "Point":
            self.processGeoJSONPoint(geometry,props)
        if gtype == "MultiPoint":
            self.processGeoJSONMultiPoint(geometry,props)
        if gtype == "LineString":
            self.processGeoJSONLineString(geometry,props)
        if gtype == "MultiLineString":
            self.processGeoJSONMultiLineString(geometry,props)
        if gtype == "Polygon":
            self.processGeoJSONPolygon(geometry,props)
        if gtype == "MultiPolygon":
            self.processGeoJSONMultiPolygon(geometry,props)
        if gtype == "GeometryCollection":
            self.processGeoJSONGeometryCollection(geometry,props)

    def processGeoJSONPolygon(self,geometry,props):
        coordinates = geometry["coordinates"]
        rings = []
        for area in coordinates:
            ring = self.processPolygon(area)
            rings.append(ring)
        self.polys.append((props,[rings]))

    def processGeoJSONMultiPolygon(self,geometry,props):
        coordinates = geometry["coordinates"]
        polys = []
        for polygon in coordinates:
            rings = []
            for area in polygon:
                ring = self.processPolygon(area)
                rings.append(ring)
            polys.append(rings)
        self.polys.append((props,polys))

    def processGeoJSONPoint(self,geometry,props):
        coordinates = geometry["coordinates"]
        point  = self.processPoint(coordinates)
        if point:
            self.points.append((props,[point]))

    def processGeoJSONMultiPoint(self,geometry,props):
        coordinates = geometry["coordinates"]
        points = []
        for coords in coordinates:
            p  = self.processPoint(coords)
            if p:
                points.append(p)
        self.points.append((props,points))

    def processGeoJSONLineString(self,geometry,props):
        coordinates = geometry["coordinates"]
        line = []
        for coord in coordinates:
            point  = self.processPoint(coord)
            if point:
                line.append(point)
        self.lines.append((props,[line]))

    def processGeoJSONMultiLineString(self,geometry,props):
        coordinates = geometry["coordinates"]
        lines = []
        for l in coordinates:
            line = []
            for coord in l:
                point  = self.processPoint(coord)
                if point:
                    line.append(point)
            lines.append(line)
        self.lines.append((props,lines))

    def processGeoJSONGeometryCollection(self,geometry,props):
        for geom in geometry["geometries"]:
            self.processGeometry(geom,props)

    def processPolygon(self,area):
        poly = []
        for point in area:
            poly.append(point)
        return poly

    def processPoint(self,coords):
        if (coords[0] != None and coords[1] != None):
            return coords
        return None

