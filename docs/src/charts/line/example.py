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

from visigoth.diagram import Diagram
from visigoth.charts.line import Line
from visigoth.containers.box import Box
from visigoth.utils.colour import DiscretePalette
from visigoth.common.legend import Legend
from visigoth.common.button import Button
from visigoth.common.text import Text
from visigoth.common.space import Space

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    parser.add_argument("--htmlpath", help="path for output HTML", default="example.html")

    args = parser.parse_args()

    palette = DiscretePalette()
    palette.addCategory("A","#E7FFAC")
    palette.addCategory("B","#FFC9DE")
    palette.addCategory("C","#B28DFF")
    palette.addCategory("D","#ACE7FF")

    r = random.Random()
    data = []
    y = -0.05
    for cat in ["A","B","C","D"]:
        for idx in range(36):
            data.append((datetime.datetime(2018,1,1,0,idx,0),y+r.random()/10,cat))
        y += 0.1
        
    d = Diagram(fill="white")

    al = Line(data,x=0,y=1,line=2,colour=2, width=600, height=600, palette=palette, x_axis_label="X", y_axis_label="Y", stroke_width=4, point_radius=2)
    ax = al.getXAxis()
    # ax.setTickPositions([datetime.datetime(2018,idx+1,1,0,0,0) for idx in range(1,12,3)])

    d.add(Box(al))
  
    legend = Legend(palette,400,legend_columns=2)
    d.add(legend)
    d.connect(legend,"brushing",al,"brushing")
    d.connect(al,"brushing",legend,"brushing")

    svg = d.draw()
    html = d.draw(format="html",html_title="Visigoth - Line Chart Example")

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()
