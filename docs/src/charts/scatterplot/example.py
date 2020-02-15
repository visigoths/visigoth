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

import os.path
import sys
import argparse
import random

from visigoth.diagram import Diagram
from visigoth.charts.scatterplot import ScatterPlot
from visigoth.containers.box import Box
from visigoth.utils.colour import DiscretePalette
from visigoth.common.legend import Legend
from visigoth.common.button import Button
from visigoth.common.text import Text
from visigoth.common.space import Space

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    palette = DiscretePalette()
    palette.addCategory("A","#E7FFAC")
    palette.addCategory("B","#FFC9DE")
    palette.addCategory("C","#B28DFF")
    palette.addCategory("D","#ACE7FF")

    r = random.Random()
    data = []
    for idx in range(0,100):
        data.append((r.random(),r.random(),"p"+str(idx),r.choice(["A","B","C","D"]),r.choice([3,5,9])))

    data.append((0.0,0.0,"origin",r.choice(["A","B","C","D"]),4))

    d = Diagram(fill="white")

    scatter = ScatterPlot(data, 500, 500, palette, x_axis_label="X AXIS", y_axis_label="Y AXIS")
    d.add(Space(20,20))
    legend = Legend(palette,400,legend_columns=2)
    d.add(legend)
    d.connect(legend,"brushing",scatter,"brushing")
    d.connect(scatter,"brushing",legend,"brushing")


    xaxis = scatter.getXAxis()
    xaxis.setStroke("red",3)
    yaxis = scatter.getYAxis()
    yaxis.setStroke("blue",3)
    d.add(scatter)
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

