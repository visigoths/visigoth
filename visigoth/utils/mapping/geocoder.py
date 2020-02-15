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
