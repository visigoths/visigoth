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
import datetime
import math

from visigoth.diagram import Diagram
from visigoth.charts.area import Area
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

    for idx in range(0,32):
        linedata = {}
        angle = idx/2.0
        for cat in ["A","B","C","D"]:
            if cat == "B" or cat == "C":
                angle += math.pi/4

            if cat == "A" or cat == "C":
                h = 1.5+math.sin(angle)
            else:
                h = 1.5+math.cos(angle)
            linedata[cat]=("",h)
        data.append((angle,linedata))

    d = Diagram(fill="white")

    al = Area(data, 600, 600, palette, negcats=["C","D"],x_axis_label="X", y_axis_label="Y")

    d.add(al)
    d.add(Space(20))
    legend = Legend(palette,400,legend_columns=2)
    d.add(legend)
    d.connect(legend,"brushing",al,"brushing")
    d.connect(al,"brushing",legend,"brushing")

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

