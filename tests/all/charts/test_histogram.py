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
import random

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.charts import Histogram
from visigoth.common import Legend, Text
from visigoth.containers import Box

class TestHistogram(unittest.TestCase):

    def test_page(self):
        d = Diagram(fill="white")

        r = random.Random()
        data = []
        for idx in range(0, 200):
            data.append({"probability": r.gauss(1, 0.2), "category": "one"})

        for idx in range(0, 100):
            data.append({"probability": r.gauss(2, 0.4), "category": "two"})

        histogram = Histogram(data, x="probability", colour="category")
        histogram.getPalette().setOpacity(0.5)
        legend = Legend(histogram.getPalette(), width=300)

        d.add(histogram)
        d.add(legend)

        d.connect(legend, "colour", histogram, "colour")
        d.connect(histogram, "colour", legend, "colour")

        TestUtils.draw_output(d, "test_histogram")

if __name__ == "__main__":
    unittest.main()