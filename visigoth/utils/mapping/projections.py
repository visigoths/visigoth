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

class PROJ_ESPG_3857(Projection):

    C1 = 20037508.34

    def __init__(self):
        super(PROJ_ESPG_3857,self).__init__("EPSG:3857")

    def fromLonLat(self,lon_lat):
        (lon,lat) = lon_lat
        e = lon * PROJ_ESPG_3857.C1 / 180
        n = math.log(math.tan((90+lat) * math.pi / 360.0)) / (math.pi / 180)
        n = n * PROJ_ESPG_3857.C1 / 180
        return (e,n)

    def toLonLat(self,e_n):
        (e,n) = e_n
        lon = e * 180 / PROJ_ESPG_3857.C1
        lat = n * 180 / PROJ_ESPG_3857.C1
        lat = 180/math.pi * (2 * math.atan(math.exp(lat*math.pi/180)) - math.pi/2)
        return (lon,lat)

class PROJ_ESPG_4326(Projection):

    def __init__(self):
        super(PROJ_ESPG_4326,self).__init__("EPSG:4326")

    def fromLonLat(self,lon_lat):
        return lon_lat

    def toLonLat(self,e_n):
        return e_n

class Projections(object):

    ESPG_3857 = PROJ_ESPG_3857()
    ESPG_4326 = PROJ_ESPG_4326()
    IDENTITY = PROJ_ESPG_4326()

    knownProjections = {
        "3857": ESPG_3857,
        "4326": ESPG_4326,
    }

    @staticmethod
    def getProjection(name):
        return Projections.knownProjections.get(name)
