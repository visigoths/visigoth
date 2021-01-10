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

import datetime
from math import floor, log10, floor, ceil
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
        self.integer_interval = None

    def setIntegerInterval(self,interval):
        self.integer_interval = interval

    def projectLat(self,lat):
        return self.projection.fromLonLat((0.0,lat))[1]

    def projectLon(self,lon):
        return self.projection.fromLonLat((lon,0.0))[0]

    def getIntegerTicks(self):
        return [p for p in range(ceil(self.lwb),1+floor(self.upb),self.integer_interval)]

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
        elif self.integer_interval is not None:
            self.tickpoints = self.getIntegerTicks()
        else:
            rng = self.upb - self.lwb
            spacing = 10**floor(log10(rng))
            stops = floor(rng/spacing)
            while stops < 5:
                spacing *= 0.1
                stops = floor(rng/spacing)
            base_spacing = spacing
            if stops > 10:
                spacing = base_spacing*2
                stops = floor(rng / spacing)
            if stops > 10:
                spacing = base_spacing*5
                stops = floor(rng / spacing)
            if stops > 10:
                spacing = base_spacing * 10
                stops = floor(rng / spacing)

            point = self.lwb - (self.lwb % spacing)
            self.tickpoints = []
            while point <= self.upb:
                self.tickpoints.append(point)
                point += spacing
            self.spacing = spacing
        return self.tickpoints

    def getSpacing(self):
        return self.spacing

    def build(self):
        if not self.tickpoints:
            self.computeTickPoints()
        return self.tickpoints[:]
