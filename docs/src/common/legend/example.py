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

from visigoth import Diagram

from visigoth.common import Legend
from visigoth.common import Space

from visigoth.utils.colour import ContinuousPalette, DiscretePalette

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    discrete_palette = DiscretePalette()
    discrete_palette.addCategory("A", "green").addCategory("B", "blue").addCategory("C", "red").addCategory("D", "orange").addCategory("E","purple")

    continuous_palette = ContinuousPalette()
    continuous_palette.addColour("#FF0000",0.0).addColour("#0000FF",1.0)

    d = Diagram(fill="white")
    d.add(Legend(discrete_palette,width=700, legend_columns=3))
    d.add(Space(50))
    d.add(Legend(continuous_palette,700))

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

