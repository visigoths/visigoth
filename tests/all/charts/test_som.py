# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

import random

import unittest

from visigoth.diagram import Diagram
from visigoth.charts.som import SOM
from visigoth.common.legend import Legend
from visigoth.utils.colour import DiscretePalette, ContinuousPalette, Colour
from visigoth.utils.test_utils import TestUtils

class TestScatterPlot(unittest.TestCase):

    def test_basic(self):

        variables = ["A","B","C","D","E"]

        palette = DiscretePalette()

        palette.addColour("A","green").addColour("B","blue").addColour("C","red").addColour("D","purple").addColour("E","yellow")

        cpalette = ContinuousPalette(withIntervals=False)

        rng = random.Random(1)

        def normalise(values):
            total = sum(values)
            return list(map(lambda x:x/total,values))

        def generateProbabilities(label,cat):
            index = variables.index(cat)
            probabilities = [rng.random() for i in range(len(variables))]
            maxprob = max(probabilities)
            if maxprob != probabilities[index]:
                probabilities[index] = maxprob*(1+0.2*rng.random())
            return (label,cat,normalise(probabilities))

        data = [ generateProbabilities("label%d"%(x),rng.choice(variables)) for x in range(500) ]

        d = Diagram(fill="white")

        som = SOM(data,width=512,gridheight=10,gridwidth=10,palette=palette,dimension=lambda l: l[0],dimensionPalette=cpalette)
        som.getMarkerManager().setDefaultRadius(5)

        d.add(som)
        d.add(Legend(cpalette,width=500))

        legend1 = Legend(palette,width=500,legend_columns=2)
        d.add(legend1)
        d.connect(legend1,"colour",som,"colour")
        d.connect(som,"colour",legend1,"colour")

        TestUtils.draw_output(d,"test_som")

if __name__ == "__main__":
    unittest.main()