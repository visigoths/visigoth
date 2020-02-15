# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

from visigoth.diagram import Diagram
from visigoth.common import Button, ButtonGrid

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    d = Diagram(fill="white")

    bg = ButtonGrid()
    bg.addButton(0,1,Button("North Button"))
    bg.addButton(1,0,Button("West Button"))
    bg.addButton(1,1,Button("Centre Button"),initially_selected=True)
    bg.addButton(1,2,Button("East Button"))
    bg.addButton(2,1,Button("South Button"))

    d.add(bg)
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()
