# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

        palette.addCategory("A","green").addCategory("B","blue").addCategory("C","red").addCategory("D","purple").addCategory("E","yellow")

        cpalette = ContinuousPalette(withIntervals=False)
        cpalette.addColour("#000000",0.0).addColour("green",0.5)

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

        svg = d.draw()

        TestUtils.output(svg,"test_som.svg")

if __name__ == "__main__":
    unittest.main()