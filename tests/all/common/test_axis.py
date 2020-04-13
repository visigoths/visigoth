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

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.common import Axis

class TestAxis(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")
        d.add(Axis(500,"horizontal",0,90,label="h-axis"))
        d.add(Axis(500,"vertical", 0, 100, label="v-axis"))
        svg = d.draw()
        TestUtils.output(svg,"test_axis.svg")

if __name__ == "__main__":
    unittest.main()
