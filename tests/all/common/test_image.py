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

        TestUtils.draw_output(d,"test_image")

if __name__ == "__main__":
    unittest.main()
