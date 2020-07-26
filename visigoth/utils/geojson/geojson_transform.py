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

import argparse

from visigoth.utils.geojson import GeojsonReader, GeojsonWriter

class GeoJsonTransformer(object):

    def __init__(self,filter_box=None,decimal_places=None,include_properties=None):
        self.filter_box=filter_box
        self.decimal_places = decimal_places
        self.include_properties = include_properties

    def transform_file(self,input_path,output_path):
        gjr = GeojsonReader()
        gjw = GeojsonWriter()
        (points, lines, polys) = gjr.extract(input_path)

        filterfn = None
        if self.filter_box:
            min_lon = self.filter_box[0]
            min_lat = self.filter_box[1]
            max_lon = self.filter_box[2]
            max_lat = self.filter_box[3]

            def filterfn(lonlats):
                for (lon, lat) in lonlats:
                    if lon >= min_lon and lon <= max_lon and lat >= min_lat and lat <= max_lat:
                        return True
                return False

        propertyfilter = None
        if self.include_properties != None:
            def propertyfilter(properties):
                removal_keys = [key for key in properties if key not in self.include_properties]
                for key in removal_keys:
                    del properties[key]

        gjw.export(output_path, points, lines, polys, featurefilter=filterfn,
                   decimal_places=self.decimal_places,
                   propertyfilter=propertyfilter)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("input_geojson_path")
    parser.add_argument("output_geojson_path")
    parser.add_argument("--filter_box",nargs=4,type=float,default=None)
    parser.add_argument("--decimal_places",type=int, default=3)
    parser.add_argument("--include_properties", default="")

    args = parser.parse_args()
    include_properties=None
    if args.include_properties != "":
        include_properties=args.include_properties.split(",")

    transformer = GeoJsonTransformer(boundaries=args.filter_box,decimal_places=args.decimal_places,include_properties=include_properties)
    transformer.transform_file(args.input_geojson_file,args.output_geojson_file)

