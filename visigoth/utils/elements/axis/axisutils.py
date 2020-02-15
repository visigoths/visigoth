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


import json
import datetime
from math import pi, floor, log10, ceil
from visigoth.utils.mapping import Projections

class AxisUtils(object):

    def __init__(self,length,orientation,lwb,upb,projection=Projections.IDENTITY,date_based=False):
        self.length = length
        self.orientation = orientation
        self.lwb = lwb
        self.upb = upb
        self.tickpoints = []
        self.projection = projection
        self.spacing = 1
        self.date_based = date_based
        self.MIN_TICKS = 10

    def projectLat(self,lat):
        return self.projection.fromLonLat((0.0,lat))[1]

    def projectLon(self,lon):
        return self.projection.fromLonLat((lon,0.0))[0]

    def getDateTicks(self):
        r = self.upb - self.lwb
        if r > 60*60*24*365*4:
            return self.getDateTicksIncrement("year")
        elif r > 60*60*24*31*6:
            return self.getDateTicksIncrement("month")
        elif r > 60*60*24*5:
            return self.getDateTicksIncrement("day")
        elif r > 60*60*5:
            return self.getDateTicksIncrement("hour")
        elif r > 60*5:
            return self.getDateTicksIncrement("minute")

        return [self.lwb,self.upb]

    def dateSnap(self,dt,increment):
        if increment == "minute":
            return datetime.datetime(dt.year,dt.month,dt.day,dt.hour,dt.minute,0)
        if increment == "hour":
            return datetime.datetime(dt.year,dt.month,dt.day,dt.hour,0,0)
        if increment == "day":
            return datetime.datetime(dt.year,dt.month,dt.day,0,0,0)
        if increment == "month":
            return datetime.datetime(dt.year,dt.month,1,0,0,0)
        if increment == "year":
            return datetime.datetime(dt.year,1,1,0,0,0)
        return dt

    def dateIncrement(self,dt,increment):
        if increment == "year":
            return datetime.datetime(dt.year+1,dt.month,dt.day,dt.hour,dt.minute,dt.second)

        if increment == "month":
            if dt.month < 12:
                return datetime.datetime(dt.year,dt.month+1,dt.day,dt.hour,dt.minute,dt.second)
            else:
                return datetime.datetime(dt.year+1,1,dt.day,dt.hour,0,0)

        if increment == "day":
            return dt + datetime.timedelta(days=1)

        if increment == "hour":
            return dt + datetime.timedelta(hours=1)

        if increment == "minute":
            return dt + datetime.timedelta(minutes=1)

        if increment == "second":
            return dt + datetime.timedelta(minutes=1)

        return dt

    def getDateTicksIncrement(self,increment):
        ticks = []
        dt = datetime.datetime.fromtimestamp(self.lwb)
        dt1 = self.dateSnap(dt,increment)
        if dt1.timestamp() < self.lwb:
            dt1 = self.dateIncrement(dt,increment)
        i1 = dt1.timestamp()
        while i1 <= self.upb:
            ticks.append(dt1)
            dt1 = self.dateIncrement(dt1,increment)
            i1 = dt1.timestamp()
        while len(ticks) > 2*self.MIN_TICKS:
            ticks = ticks[0:1] + [ticks[idx] for idx in range(1,len(ticks)-1,2)] + ticks[-1:]
        return ticks

    def getPointPosition(self,start,value):
        if self.date_based:
            value = value.timestamp()
        if self.orientation == "horizontal":
            return start + self.length*((self.projectLon(value)-self.projectLon(self.lwb))/(self.projectLon(self.upb)-self.projectLon(self.lwb)))
        else:
            return start + self.length - self.length*((self.projectLat(value)-self.projectLat(self.lwb))/(self.projectLat(self.upb)-self.projectLat(self.lwb)))

    def getTickPositions(self,start):
        positions = []
        for tv in self.tickpoints:
            positions.append(self.getPointPosition(start,tv))
        return positions

    def setTickPoints(self,tickpoints):
        self.tickpoints = tickpoints

    def computeTickPoints(self):
        if self.date_based:
            self.tickpoints = self.getDateTicks()
        else:
            rng = self.upb - self.lwb
            spacing = 10**floor(log10(rng))
            stops = floor(rng/spacing)
            while stops < 5:
                spacing *= 0.5
                stops = floor(rng/spacing)
            point = self.lwb - (self.lwb % spacing)
            self.tickpoints = []
            while point <= self.upb:
                if point >= self.lwb:
                    self.tickpoints.append(point)
                point += spacing
            self.spacing = spacing
        return self.tickpoints[:]

    def getSpacing(self):
        return self.spacing

    def build(self):
        return self.computeTickPoints()
