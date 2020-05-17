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
from visigoth.charts import Table
from visigoth.common import Legend, Text
from visigoth.containers import Box

class TestTable(unittest.TestCase):

    def test_page(self):
        d = Diagram(fill="white")

        headings = [(0 ,"column1" ,lambda x :"%0.2f " %x) ,(1 ,"column2") ,(2 ,"category")]
        data = [[0.12345 ,"bar" ,"aaa"] ,[351 ,"the quick brown fox jumped over the lazy dog" ,"aaa"] ,[100 ,"four" ,"bbb"]]

        t = Table(data ,headings=headings ,colour=2 ,max_column_width=200)
        t.setLeftJustified()

        l = Legend(t.getPalette())
        d.add(t).add(l)

        svg = d.draw()

        TestUtils.output(svg, "test_table.svg")

if __name__ == "__main__":
    unittest.main()