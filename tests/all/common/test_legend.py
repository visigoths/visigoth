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
from visigoth.common import Legend, Text, Space
from visigoth.containers.box import Box
from visigoth.containers.sequence import Sequence
from visigoth.utils.colour import ContinuousPalette, DiscretePalette


class TestLegend(unittest.TestCase):

    def test_discrete(self):
        d = Diagram(fill="white")

        discrete_palette1 = DiscretePalette()
        discrete_palette1.addColour("A", "green").addColour("B", "blue").addColour("C", "red").addColour("D", "orange").addColour("E","purple")

        d.add(Box(Legend(discrete_palette1,width=700, legend_columns=3)))
        d.add(Box(Legend(discrete_palette1,width=700, legend_columns=2)))
        d.add(Box(Legend(discrete_palette1,width=700, legend_columns=1)))

        cmaps = DiscretePalette.listColourMaps()
        for cmap in cmaps:
            p = DiscretePalette(colourMap=cmap)
            for v in ["A","B","C","D","E","F"]:
                p.getColour(v)
            d.add(Text("colour-map="+cmap))
            d.add(Box(Legend(p, width=700, legend_columns=2)))
        svg = d.draw()
        TestUtils.output(svg,"test_legend_discrete.svg")

    def test_continuous(self):

        d = Diagram(fill="white")

        cp = ContinuousPalette(withIntervals=False)
        cp.getColour(0.0)
        cp.getColour(7.0)
        d.add(Text("no intervals"))
        d.add(Legend(cp, 700))

        for (minv,maxv) in [(0.0,6.0),(0.00017,0.00042),(-10,-5),(3.0,4.5),(-1.0,2.0),(200,1000)]:
            cp = ContinuousPalette()
            cp.getColour(minv)
            cp.getColour(maxv)
            d.add(Text("palette %f -> %f"%(minv,maxv)))
            d.add(Legend(cp, 700))

        custom_colourmap = ContinuousPalette(colourMap=[(0.0,0.0,1.0),(0.0,1.0,0.0),(1.0,0.0,0.0)])
        custom_colourmap.getColour(0)
        custom_colourmap.getColour(5)
        d.add(Text("custom colourmap Blue -> Green -> Red"))
        d.add(Legend(custom_colourmap,700,orientation="horizontal"))

        seq = Sequence(orientation="horizontal")
        continuous_palette5 = ContinuousPalette()
        continuous_palette5.getColour(-1.0)
        continuous_palette5.getColour(2.0)
        seq.add(Box(Legend(continuous_palette5, 200, orientation="vertical")))

        continuous_palette6 = ContinuousPalette()
        continuous_palette6.getColour(200)
        continuous_palette6.getColour(1000)
        seq.add(Box(Legend(continuous_palette6, 200, orientation="vertical")))

        continuous_palette7 = ContinuousPalette()
        continuous_palette7.getColour(0.0)
        continuous_palette7.getColour(3.0)
        seq.add(Box(Legend(continuous_palette7, 200, orientation="vertical")))
        d.add(Text("Vertical orientation"))
        d.add(seq)

        cmaps = ContinuousPalette.listColourMaps()
        for cmap in cmaps:
            p = ContinuousPalette(colourMap=cmap)
            p.getColour(0.0)
            p.getColour(100.0)
            d.add(Text("colour-map=" + cmap))
            d.add(Box(Legend(p, width=700)))

        svg = d.draw()
        TestUtils.output(svg,"test_legend_continuous.svg")

if __name__ == "__main__":
    unittest.main()
