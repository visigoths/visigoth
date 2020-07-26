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
import re


class GeojsonWriter(object):

    def __init__(self):
        pass

    def export(self,path, multipoints, multilines, multipolys, featurefilter=None, propertyfilter=None, decimal_places=5):
        exported = {}
        exported["type"] = "FeatureCollection"
        features = []

        for multipoint in multipoints:
            properties = multipoint[0]
            coordinates = multipoint[1]
            flat_coords = [(lon,lat) for (lon,lat) in coordinates]
            if featurefilter and not featurefilter(flat_coords):
                continue
            if propertyfilter:
                propertyfilter(properties)
            geometry = { "type":"MultiPoint", "coordinates":coordinates }
            feature = { "type":"Feature", "properties":properties, "geometry":geometry }
            features.append(feature)

        for multiline in multilines:
            properties = multiline[0]
            coordinates = multiline[1]
            flat_coords = [(lon,lat) for l1 in coordinates for (lon,lat) in l1]
            if featurefilter and not featurefilter(flat_coords):
                continue
            if propertyfilter:
                propertyfilter(properties)
            geometry = { "type":"MultiLineString", "coordinates":coordinates }
            feature = { "type":"Feature", "properties":properties, "geometry":geometry }
            features.append(feature)

        for multipoly in multipolys:
            properties = multipoly[0]
            coordinates = multipoly[1]
            flat_coords = [(lon,lat) for l1 in coordinates for l2 in l1 for (lon,lat) in l2]
            if featurefilter and not featurefilter(flat_coords):
                continue
            if propertyfilter:
                propertyfilter(properties)
            geometry = { "type":"MultiPolygon", "coordinates":coordinates }
            feature = { "type":"Feature", "properties":properties, "geometry":geometry }
            features.append(feature)

        exported["features"] = features

        jgs = json.dumps(exported)

        # by default JSON floats are encoded at double precision by python's json encoder
        # postprocess to modify the precision using regexp

        # build a pattern to match higher precision floating point numbers
        threshold = decimal_places+1
        pat = re.compile(r"\d+\.\d{%d,}"%(threshold))

        # and a function to perform the substitution
        def mround(match):
            return ("{:.%df}"%(decimal_places)).format(float(match.group()))

        # write the modified string to a file
        f = open(path, 'w')
        f.write(re.sub(pat, mround, jgs))
        f.close()
