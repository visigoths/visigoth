# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

import unittest
import random

from visigoth import Diagram

from visigoth.containers.map import Map
from visigoth.utils.mapping import Mapping
from visigoth.map_layers import Geoplot
from visigoth.map_layers.geoplot import Multipoint
from visigoth.containers.popup import Popup
from visigoth.containers.box import Box
from visigoth.common.text import Text
from visigoth.common import SearchController

from visigoth.utils.mapping import Projections
from visigoth.utils.test_utils import TestUtils


class TestSearchController(unittest.TestCase):

    def test_basic(self):
        rng = random.Random()
        d = Diagram(fill="white")

        center = (0,0)
        bounds = Mapping.computeBoundaries(center,4000)

        lon_min = bounds[0][0]
        lon_max = bounds[1][0]
        lat_min = bounds[0][1]
        lat_max = bounds[1][1]

        lon_range = lon_max-lon_min
        lat_range = lat_max-lat_min

        multipoints=[]
        for i in range(20):
            popup = Popup(Text("Popup! %d"%(i)),"popup")
            label = "point_%d"%i
            col = rng.choice(["red","purple","orange","green"])
            lon = lon_min+rng.random()*lon_range
            lat = lat_min+rng.random()*lat_range
            multipoints.append(Multipoint([(lon,lat)],label=label,popup=popup,properties={"type":"point"},fill=col))

        gp = Geoplot(multipoints=multipoints)

        m = Map(768,boundaries=bounds,projection=Projections.EPSG_3857)

        sm = SearchController(height=150)
        d.add(sm)

        m.add(gp)
        d.add(Box(m))
        d.connect(sm,"search",m,"search")

        TestUtils.draw_output(d,"test_search_manager")

if __name__ == "__main__":
    unittest.main()
