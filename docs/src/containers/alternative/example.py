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

import argparse
from visigoth import Diagram

from visigoth.containers import Alternative, Box, Sequence
from visigoth.charts import Pie, Bar
from visigoth.common import Button, ButtonGrid, Legend
from visigoth.utils.colour import DiscretePalette

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    d = Diagram(fill="white")

    palette0 = DiscretePalette()
    palette0.addCategory("A","#E7FFAC").addCategory("B","#FFC9DE")
    palette0.addCategory("C","#B28DFF").addCategory("D","#ACE7FF")

    legend = Legend(palette0,legend_columns=2)

    data0 = [("A",1.2),("B",0.7),("C",0.4),("D",0.5)]

    bar0 = Bar(data0, 400, 400, palette0,labelfn=lambda k,v:"%0.2f"%v)
    pie0 = Pie(data0, 400, 400, palette0)

    a = Alternative()
    a.add(pie0)
    a.add(bar0)

    seq0 = Sequence(orientation="horizontal")
    b1 = Button(text="pie chart",click_value=pie0.getId())
    b2 = Button(text="bar chart",click_value=bar0.getId())

    bg = ButtonGrid()
    bg.addButton(0,0,b1,initially_selected=True)
    bg.addButton(0,1,b2)

    d.add(bg)

    d.add(Box(a,fill="lightgrey"))
    d.add(legend)
    d.connect(bg,"click",a,"show")
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()