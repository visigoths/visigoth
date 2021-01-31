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
from visigoth.common import Legend, Text, Space
from visigoth.containers.box import Box
from visigoth.containers.sequence import Sequence
from visigoth.utils.colour import ContinuousColourManager, DiscreteColourManager


class TestLegend(unittest.TestCase):

    def test_discrete(self):
        d = Diagram(fill="white")

        discrete_colour_manager1 = DiscreteColourManager()
        discrete_colour_manager1.addColour("A", "green").addColour("B", "blue").addColour("C", "red").addColour("D", "orange").addColour("E","purple")

        d.add(Box(Legend(discrete_colour_manager1,width=700, legend_columns=3)))
        d.add(Box(Legend(discrete_colour_manager1,width=700, legend_columns=2)))
        d.add(Box(Legend(discrete_colour_manager1,width=700, legend_columns=1)))

        cmaps = DiscreteColourManager.listColourMaps()
        for cmap in cmaps:
            p = DiscreteColourManager(colourMap=cmap)
            for v in ["A","B","C","D","E","F"]:
                p.allocateColour(v)
            d.add(Text("colour-map="+cmap))
            d.add(Box(Legend(p, width=700, legend_columns=2)))

        TestUtils.draw_output(d,"test_legend_discrete")

    def test_continuous(self):

        d = Diagram(fill="white")

        cp = ContinuousColourManager(withIntervals=False)
        cp.allocateColour(0.0)
        cp.allocateColour(7.0)
        d.add(Text("no intervals"))
        d.add(Legend(cp, 700))

        for (minv,maxv) in [(0.0,6.0),(0.00017,0.00042),(-10,-5),(3.0,4.5),(-1.0,2.0),(200,1000)]:
            cp = ContinuousColourManager()
            cp.allocateColour(minv)
            cp.allocateColour(maxv)
            d.add(Text("colour_manager %f -> %f"%(minv,maxv)))
            d.add(Legend(cp, 700))

        custom_colourmap = ContinuousColourManager(colourMap=[(0.0,0.0,1.0),(0.0,1.0,0.0),(1.0,0.0,0.0)])
        custom_colourmap.allocateColour(0)
        custom_colourmap.allocateColour(5)
        d.add(Text("custom colourmap Blue -> Green -> Red"))
        d.add(Legend(custom_colourmap,700,orientation="horizontal"))

        seq = Sequence(orientation="horizontal")
        continuous_colour_manager5a = ContinuousColourManager(withIntervals=False)
        continuous_colour_manager5a.allocateColour(-1.0)
        continuous_colour_manager5a.allocateColour(2.0)
        seq.add(Box(Legend(continuous_colour_manager5a, 200, orientation="vertical")))

        continuous_colour_manager5 = ContinuousColourManager()
        continuous_colour_manager5.allocateColour(-1.0)
        continuous_colour_manager5.allocateColour(2.0)
        seq.add(Box(Legend(continuous_colour_manager5, 200, orientation="vertical")))

        continuous_colour_manager6 = ContinuousColourManager()
        continuous_colour_manager6.allocateColour(200)
        continuous_colour_manager6.allocateColour(1000)
        seq.add(Box(Legend(continuous_colour_manager6, 200, orientation="vertical")))

        continuous_colour_manager7 = ContinuousColourManager()
        continuous_colour_manager7.allocateColour(0.0)
        continuous_colour_manager7.allocateColour(3.0)
        seq.add(Box(Legend(continuous_colour_manager7, 200,orientation="vertical")))
        d.add(Text("Vertical orientation"))
        d.add(seq)

        cmaps = ContinuousColourManager.listColourMaps()
        for cmap in cmaps:
            p = ContinuousColourManager(colourMap=cmap)
            p.allocateColour(0.0)
            p.allocateColour(100.0)
            d.add(Text("colour-map=" + cmap))
            d.add(Box(Legend(p, width=700)))

        continuous_colour_manager8 = ContinuousColourManager(colourMap=["green","blue"],underflowColour="yellow",overflowColour="red")
        continuous_colour_manager8.allocateColour(5000000)
        continuous_colour_manager8.allocateColour(10000000)
        b = Box(Legend(continuous_colour_manager8, 200, orientation="horizontal"))
        d.add(Text("Under/overshoot colours"))
        d.add(b)

        continuous_colour_manager9 = ContinuousColourManager(colourMap=["green", "blue"], underflowColour="yellow",
                                                overflowColour="red", ticks=[200000,500000,650000,800000,1100000])
        b = Box(Legend(continuous_colour_manager9, 300, orientation="horizontal"))
        d.add(Text("Custom tick positions"))
        d.add(b)

        continuous_colour_manager10 = ContinuousColourManager(colourMap=["green", "blue"], underflowColour="yellow",
                                                overflowColour="red", ticks=[200000, 500000, 650000, 800000, 1100000])
        b = Box(Legend(continuous_colour_manager10, 300, orientation="horizontal",labelfn=lambda v:"%0.1fM"%(v/1e6)))
        d.add(Text("Custom labels"))
        d.add(b)

        # https://github.com/visualtopology/visigoth/issues/1
        d.add(Legend(ContinuousColourManager(min_val=215, max_val=320)))

        TestUtils.draw_output(d,"test_legend_continuous")



if __name__ == "__main__":
    unittest.main()
