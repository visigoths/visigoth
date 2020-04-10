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
from visigoth.common.legend import Legend
from visigoth.common.space import Space
from visigoth.containers.box import Box
from visigoth.containers.sequence import Sequence
from visigoth.utils.colour import ContinuousPalette, DiscretePalette


class TestLegend(unittest.TestCase):

    def test_discrete(self):
        d = Diagram(fill="white")

        discrete_palette = DiscretePalette()
        discrete_palette.addCategory("A", "green").addCategory("B", "blue").addCategory("C", "red").addCategory("D", "orange").addCategory("E","purple")
        d.add(Legend(discrete_palette,width=700, legend_columns=3))
        d.add(Space(50))
        d.add(Legend(discrete_palette,width=700, legend_columns=2))
        d.add(Space(50))
        d.add(Legend(discrete_palette,width=700, legend_columns=1))
        svg = d.draw()
        TestUtils.output(svg,"test_legend_discrete.svg")

    def test_continuous(self):

        continuous_palette = ContinuousPalette()
        continuous_palette.addColour("#FF0000",0.0).addColour("#0000FF",1.0)

        continuous_palette2 = ContinuousPalette()
        continuous_palette2.addColour("#FF0000",0.7).addColour("#0000FF",100.1).addColour("#00FF00",200.1)

        continuous_palette3 = ContinuousPalette()
        continuous_palette3.addColour("#FF00FF",0.7).addColour("#00FF00",0.8)

        continuous_palette4 = ContinuousPalette()
        continuous_palette4.addColour("#FF00FF",-12.0).addColour("#00FF00",4.0).addColour("#000000",0.0)

        d = Diagram(fill="white")
        d.add(Legend(continuous_palette,700))
        seq = Sequence(orientation="horizontal")
        seq.add(Box(Legend(continuous_palette,200,orientation="vertical")))
        seq.add(Box(Legend(continuous_palette2,200,orientation="vertical")))
        seq.add(Box(Legend(continuous_palette3,200,orientation="vertical")))
        d.add(seq)
        d.add(Box(Legend(continuous_palette2,700)))
        d.add(Box(Legend(continuous_palette3,700)))
        d.add(Box(Legend(continuous_palette4,700)))

        svg = d.draw()
        TestUtils.output(svg,"test_legend_continuous.svg")

if __name__ == "__main__":
    unittest.main()
