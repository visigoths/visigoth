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
from urllib.parse import urlencode

from visigoth.utils.httpcache import HttpCache

class Geocoder(object):

    def __init__(self):
        self.url = "https://nominatim.openstreetmap.org/search?%s"

    def fetchBoundingBox(self,location):
        cache = HttpCache()
        p = { "q":location, "format":"json"}
        results  = cache.fetch(self.url%(urlencode(p)))
        j = json.loads(results.decode("utf-8"))
        bbox = list(map(lambda coord:float(coord),j[0]["boundingbox"]))
        return ((bbox[2],bbox[0]),(bbox[3],bbox[1]))

    def fetchCenter(self,location):
        cache = HttpCache()
        p = { "q":location, "format":"json"}
        results  = cache.fetch(self.url%(urlencode(p)))
        j = json.loads(results.decode("utf-8"))
        lat = float(j[0]["lat"])
        lon = float(j[0]["lon"])
        return (lon,lat)
