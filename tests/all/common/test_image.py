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
import os

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.common.image import Image
from visigoth.common.space import Space
from visigoth.containers.box import Box


class TestImage(unittest.TestCase):

    def test_basic(self):
        folder = os.path.split(__file__)[0]
        d = Diagram(fill="white")
        with open(os.path.join(folder,"up.png"),"rb") as image1file:
            image1data = image1file.read()
            d.add(Box(Image("image/png",image1data,width=64,height=64,tooltip="Up")))
            d.add(Space(20))
            d.add(Box(Image("image/png",image1data,width=16,height=16,tooltip="Up")))
        d.add(Space(20))
        with open(os.path.join(folder,"down.png"),"rb") as image2file:
            image2data = image2file.read()
            d.add(Box(Image("image/png",image2data,width=16,height=16,tooltip="Down")))
            d.add(Space(20))
            d.add(Box(Image("image/png",image2data,width=64,height=64,tooltip="Down")))

        svg = d.draw()
        TestUtils.output(svg,"test_image.svg")

if __name__ == "__main__":
    unittest.main()
