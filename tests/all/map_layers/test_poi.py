# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

import unittest

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.containers import Map
from visigoth.containers import Box
from visigoth.common import Space
from visigoth.map_layers import WMS, POI
from visigoth.utils.mapping import Geocoder, Mapping

class TestPOI(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        gc = Geocoder()
        center = gc.fetchCenter("Rio de Janeiro")
        bounds = Mapping.computeBoundaries(center,2000000)
        m = Map(512,boundaries=bounds)

        poi = POI()
        poi.addImage("https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Rio_Collage.png/280px-Rio_Collage.png",-43.196389,-22.908333,title="Rio de Janeiro",scale=0.75)
        poi.addImage("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Bras%C3%ADlia_Collage.png/280px-Bras%C3%ADlia_Collage.png",-47.882778,-15.793889,title="Brasília",scale=0.75,fill="blue")
        poi.addImage("https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Montagem_SP.png/280px-Montagem_SP.png",-46.633333,-23.55,title="São Paulo",fill="purple")
        m.addLayer(WMS())
        m.addLayer(poi)
        d.add(Space(200))
        d.add(Box(m))
        
        svg = d.draw()
        TestUtils.output(svg,"test_media.svg")

if __name__ == "__main__":
    unittest.main()
