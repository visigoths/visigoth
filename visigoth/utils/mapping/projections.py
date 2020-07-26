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

import math

class Projection(object):

    def __init__(self,name):
        self.name = name

    def getName(self):
        return self.name

    def fromLonLat(self,lon_lat):
        pass

    def toLonLat(self,e_n):
        pass

class PROJ_EPSG_3857(Projection):

    C1 = 20037508.34

    def __init__(self):
        super(PROJ_EPSG_3857,self).__init__("EPSG:3857")

    def fromLonLat(self,lon_lat):
        (lon,lat) = lon_lat
        e = lon * PROJ_EPSG_3857.C1 / 180
        n = math.log(math.tan((90+lat) * math.pi / 360.0)) / (math.pi / 180)
        n = n * PROJ_EPSG_3857.C1 / 180
        return (e,n)

    def toLonLat(self,e_n):
        (e,n) = e_n
        lon = e * 180 / PROJ_EPSG_3857.C1
        lat = n * 180 / PROJ_EPSG_3857.C1
        lat = 180/math.pi * (2 * math.atan(math.exp(lat*math.pi/180)) - math.pi/2)
        return (lon,lat)

class PROJ_EPSG_4326(Projection):

    def __init__(self):
        super(PROJ_EPSG_4326,self).__init__("EPSG:4326")

    def fromLonLat(self,lon_lat):
        return lon_lat

    def toLonLat(self,e_n):
        return e_n

class Projections(object):

    EPSG_3857 = PROJ_EPSG_3857()
    EPSG_4326 = PROJ_EPSG_4326()
    IDENTITY = PROJ_EPSG_4326()

    knownProjections = {
        "3857": EPSG_3857,
        "4326": EPSG_4326,
    }

    @staticmethod
    def getProjection(name):
        return Projections.knownProjections.get(name)

    @staticmethod
    def getENBoundaries(projection,lonlat_boundaries):
        ((lon_min,lat_min),(lon_max,lat_max)) = lonlat_boundaries
        xmin = None
        ymin = None
        xmax = None
        ymax = None
        res = 2
        lon_step = (lon_max - lon_min)/res
        lat_step = (lat_max - lat_min)/res
        for x in range(0,res+1):
            lon = lon_min + (x*lon_step)
            for y in range(0,res+1):
                lat = lat_min + (y*lat_step)
                (x,y) = projection.fromLonLat((lon,lat))
                if xmin == None or x < xmin:
                    xmin = x
                if xmax == None or x > xmax:
                    xmax = x
                if ymin == None or y < ymin:
                    ymin = y
                if ymax == None or y > ymax:
                    ymax = y

        return ((xmin,ymin),(xmax,ymax))