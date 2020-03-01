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

from visigoth.diagram import Diagram
from visigoth.charts.bar import Bar
from visigoth.utils.colour import DiscretePalette
from visigoth.containers.box import Box
from visigoth.common.legend import Legend
from visigoth.common.text import Text
from visigoth.common.space import Space

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    palette = DiscretePalette()

    data = [{"c1":"A","c2":10},{"c1":"B","c2":5},{"c1":"C","c2":6},{"c1":"D","c2":8}]

    d = Diagram(fill="white")

    bar1 = Bar(data,x="c1",y="c2",colour="c1",width=400, height=400, palette=palette,labelfn=lambda k,v:"%d"%v)
    d.add(bar1)
    legend = Legend(palette,400,legend_columns=2)
    d.add(legend)

    d.connect(bar1,"brushing",legend,"brushing")
    d.connect(legend,"brushing",bar1,"brushing")
    
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

