# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
from visigoth.common import SearchManager

from visigoth.utils.mapping import Projections
from visigoth.utils.test_utils import TestUtils


class TestSearchManager(unittest.TestCase):

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

        sm = SearchManager(height=150)
        d.add(sm)

        m.add(gp)
        d.add(Box(m))
        d.connect(sm,"search",m,"search")

        TestUtils.draw_output(d,"test_search_manager")

if __name__ == "__main__":
    unittest.main()
