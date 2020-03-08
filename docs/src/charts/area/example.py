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

    data = [(0,1,"A"),(1,1.5,"A"),(2,1.6,"A"),(3,1.3,"A"),(4,1.2,"A")] + \
        [(0,4,"B"),(1,3.5,"B"),(2,2.6,"B"),(3,1.6,"B"),(4,0.8,"B")] + \
        [(0,1,"C"),(1,1.7,"C"),(2,2.6,"C"),(3,2.8,"C"),(4,3.1,"C")]
    
    d = Diagram(fill="white")

    a = Area(data)

    d.add(a)
    legend = Legend(a.getPalette(),400,legend_columns=2)
    d.add(legend)

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

