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
    
    r = random.Random()
    data = []
    for idx in range(0,100):
        data.append((r.random(),r.random(),"p"+str(idx),r.choice(["A","B","C","D"]),r.choice([3,5,9])))

    d = Diagram(fill="white")

    scatter = ScatterPlot(data,x=0,y=1,label=2,colour=3,size=4,palette=palette)
    legend = Legend(palette,400,legend_columns=2)
    d.add(legend)
    d.connect(legend,"brushing",scatter,"brushing")
    d.connect(scatter,"brushing",legend,"brushing")


    (xaxis,yaxis) = scatter.getAxes()
    xaxis.setStroke("red",3)
    yaxis.setStroke("blue",3)
    d.add(scatter)
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

