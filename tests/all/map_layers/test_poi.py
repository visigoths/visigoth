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

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.containers import Map
from visigoth.containers import Box
from visigoth.common import Space
from visigoth.map_layers import WMS, POI
from visigoth.utils.mapping import Geocoder, Mapping
from visigoth.utils.colour.palette import DiscretePalette

class TestPOI(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        gc = Geocoder()
        center = gc.fetchCenter("Rio de Janeiro")
        bounds = Mapping.computeBoundaries(center,2000000)
        m = Map(512,boundaries=bounds,zoom_to=4)

        p1 = {"url":"https://upload.wikimedia.org/wikipedia/commons/thumb/7/79/Rio_Collage.png/280px-Rio_Collage.png","lon":-43.196389,"lat":-22.908333,"label":"Rio de Janeiro","scale":0.75,"colour":"red"}
        p2 = {"url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Bras%C3%ADlia_Collage.png/280px-Bras%C3%ADlia_Collage.png","lon":-47.882778,"lat":-15.793889,"label":"Brasília","scale":0.75,"colour":"blue"}
        p3 = {"url":"https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Montagem_SP.png/280px-Montagem_SP.png","lon":-46.633333,"lat":-23.55,"label":"São Paulo","scale":0.5,"colour":"green"}

        poi = POI([p1,p2,p3],lat="lat",lon="lon",label="label",image="url",image_scale="scale",colour="colour")
        poi.getPalette().setDefaultColour("red")
        m.add(WMS())
        m.add(poi)
        d.add(Space(200))
        d.add(Box(m))

        TestUtils.draw_output(d,"test_poi")

if __name__ == "__main__":
    unittest.main()
