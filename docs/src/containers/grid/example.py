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

from visigoth.containers import Grid
from visigoth.common import Text

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    d = Diagram(fill="white")

    d.add(Text("Simple Grid"))

    g = Grid()
    g.add(0,0,Text("Top-Left Cell in Grid"))
    g.add(1,0,Text("Bottom-Left").setRightJustified())
    g.add(0,1,Text("Top-Right").setLeftJustified())
    g.add(1,1,Text("Bottom-Right Cell in Grid"))
    d.add(g)

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

