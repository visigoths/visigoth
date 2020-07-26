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

import unittest
import datetime

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.common import Text
from visigoth.containers import Map, Box, Sequence
from visigoth.map_layers.wms import WMS
from visigoth.utils.mapping import Projections

class TestWMS(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        bounds = ((166.509144322, -46.641235447), (178.517093541, -34.4506617165))

        d.add(Text("EPSG:3857"))
        s1 = Sequence(orientation="horizontal")
        m1a = Map(512, bounds)
        m1a.add(WMS(type="osm"))
        s1.add(m1a)
        m1b = Map(512, bounds)
        m1b.add(WMS(type="satellite"))
        s1.add(m1b)
        d.add(Box(s1))

        d.add(Text("EPSG:4326"))
        s2 = Sequence(orientation="horizontal")
        m2a = Map(512, bounds, projection=Projections.EPSG_4326)
        m2a.add(WMS(type="osm"))
        s2.add(m2a)
        m2b = Map(512, bounds, projection=Projections.EPSG_4326)
        m2b.add(WMS(type="satellite"))
        s2.add(m2b)
        d.add(Box(s2))

        d.add(Text("EPSG:4326 with named satellite layers"))
        s3 = Sequence(orientation="horizontal")
        m3a = Map(512, bounds, projection=Projections.EPSG_4326)
        m3a.add(WMS(type="satellite",layer_name="MODIS_Terra_SurfaceReflectance_Bands121"))
        s3.add(m3a)
        m3b = Map(512, bounds, projection=Projections.EPSG_4326)
        m3b.add(WMS(type="satellite",layer_name="MODIS_Terra_L3_SurfaceReflectance_Bands121_8Day"))
        s3.add(m3b)
        d.add(Box(s3))

        d.add(Text("Date Progression"))
        s4 = Sequence(orientation="horizontal")
        for dt in [datetime.datetime(2018,1,1),datetime.datetime(2018,4,1),datetime.datetime(2018,7,1),datetime.datetime(2018,10,1)]:
            m = Map(256, bounds, projection=Projections.EPSG_4326)
            m.add(WMS(type="satellite", layer_name="MODIS_Terra_L3_SurfaceReflectance_Bands121_8Day", date=dt))
            s=Sequence()
            s.add(Text(dt.strftime("%Y-%m-%d")))
            s.add(m)
            s4.add(s)
        d.add(Box(s4))

        print(WMS.getLayerNames("satellite",projection=Projections.EPSG_4326))
        TestUtils.draw_output(d,"test_wms")


if __name__ == "__main__":
    unittest.main()
