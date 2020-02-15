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
from visigoth.common import Button, ButtonGrid

class TestButton(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        bg = ButtonGrid()
        bg.addButton(0,0,Button("Button(row=0,col=0)"),True)
        bg.addButton(0,1,Button("Button(row=0,col=1)"))
        bg.addButton(0,2,Button("Button(row=0,col=2)"))
        bg.addButton(1,0,Button("Button(row=1,col=0)"))
        bg.addButton(1,1,Button("Button(row=1,col=1)"))
        bg.addButton(1,2,Button("Button(row=1,col=2)"))

        svg = d.draw()
        TestUtils.output(svg,"test_buttongrid.svg")
