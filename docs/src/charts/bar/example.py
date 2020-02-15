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
    palette.addCategory("A","#E7FFAC").addCategory("B","#FFC9DE")
    palette.addCategory("B1","red").addCategory("B2","green")
    palette.addCategory("C","#B28DFF").addCategory("D","#ACE7FF")
    palette.addCategory("D1","orange").addCategory("D2","purple")

    data = [("A",10),("B",[("B1",5),("B2",15)]),("C",-4),("D",[("D1",-5),("D2",-2)])]

    d = Diagram(fill="white")

    bar1 = Bar(data, 400, 400, palette,labelfn=lambda k,v:"%d"%v)
    d.add(bar1).add(Space(20))
    bar2 = Bar(data, 400, 400, palette,waterfall=True,draw_axis=True,draw_grid=False,labelfn=lambda k,v:"%d"%v)
    d.add(bar2).add(Space(20))
    legend = Legend(palette,400,legend_columns=2)
    d.add(legend)

    # connect all pairs of main elements via a brushing channel
    for e1 in [legend,bar1,bar2]:
        for e2 in [legend,bar1,bar2]:
            if e1 != e2:
                d.connect(e1,"brushing",e2,"brushing")
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

