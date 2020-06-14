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
        m1a.addLayer(WMS(type="osm"))
        s1.add(m1a)
        m1b = Map(512, bounds)
        m1b.addLayer(WMS(type="satellite"))
        s1.add(m1b)
        d.add(Box(s1))

        d.add(Text("EPSG:4326"))
        s2 = Sequence(orientation="horizontal")
        m2a = Map(512, bounds, projection=Projections.EPSG_4326)
        m2a.addLayer(WMS(type="osm"))
        s2.add(m2a)
        m2b = Map(512, bounds, projection=Projections.EPSG_4326)
        m2b.addLayer(WMS(type="satellite"))
        s2.add(m2b)
        d.add(Box(s2))

        d.add(Text("EPSG:4326 with named satellite layers"))
        s3 = Sequence(orientation="horizontal")
        m3a = Map(512, bounds, projection=Projections.EPSG_4326)
        m3a.addLayer(WMS(type="satellite",layer_name="MODIS_Terra_SurfaceReflectance_Bands121"))
        s3.add(m3a)
        m3b = Map(512, bounds, projection=Projections.EPSG_4326)
        m3b.addLayer(WMS(type="satellite",layer_name="MODIS_Terra_L3_SurfaceReflectance_Bands121_8Day"))
        s3.add(m3b)
        d.add(Box(s3))

        d.add(Text("Date Progression"))
        s4 = Sequence(orientation="horizontal")
        for dt in [datetime.datetime(2018,1,1),datetime.datetime(2018,4,1),datetime.datetime(2018,7,1),datetime.datetime(2018,10,1)]:
            m = Map(256, bounds, projection=Projections.EPSG_4326)
            m.addLayer(WMS(type="satellite", layer_name="MODIS_Terra_L3_SurfaceReflectance_Bands121_8Day", date=dt))
            s=Sequence()
            s.add(Text(dt.strftime("%Y-%m-%d")))
            s.add(m)
            s4.add(s)
        d.add(Box(s4))

        svg = d.draw()

        print(WMS.getLayerNames("satellite",projection=Projections.EPSG_4326))
        TestUtils.output(svg,"test_wms.svg")


if __name__ == "__main__":
    unittest.main()
