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

        svg = d.draw()

        TestUtils.output(svg, "test_table.svg")

if __name__ == "__main__":
    unittest.main()