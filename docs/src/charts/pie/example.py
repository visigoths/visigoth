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
from visigoth.charts.pie import Pie
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
    palette.addCategory("A","#E7FFAC").addCategory("B","#FFC9DE").addCategory("C","#B28DFF").addCategory("D","#ACE7FF")
    palette.addCategory("D.1","red").addCategory("D.2","green").addCategory("D.3","blue")
    palette.addCategory("B.2","purple").addCategory("B.1","orange")

    data = [("A",10),("B",[("B.1",15),("B.2",5)]),("C",4),("D",[("D.1",12),("D.2",3),("D.3",5)])]

    d = Diagram(fill="white")

    pie = Pie(data, 400, 400, palette, doughnut=True)
    d.add(pie)
    d.add(Space(20))
    legend = Legend(palette,400,legend_columns=2)
    d.add(legend)
    d.connect(legend,"brushing",pie,"brushing")
    d.connect(pie,"brushing",legend,"brushing")
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

