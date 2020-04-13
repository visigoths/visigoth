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

from visigoth.diagram import Diagram
from visigoth.charts import Bar, Scatter
from visigoth.utils.colour import DiscretePalette, ContinuousPalette
from visigoth.common import Text, Legend

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    rng = random.Random()
    scatterdata1 = [(rng.random(),rng.random(),"",10*rng.random(),10) for x in range(0,50)]
    scatterdata2 = [(rng.random(),rng.random(),"",rng.choice(["A","B","C","D","E","F"]),10) for x in range(0,50)]

    d = Diagram(fill="white")

    for colourMap in DiscretePalette.listColourMaps():
        palette = DiscretePalette(colourMap=colourMap) 
        scatter = Scatter(scatterdata2, 400, 400, palette)
        d.add(Text(colourMap,font_height=32))
        d.add(scatter)
        legend = Legend(palette,400)
        d.add(legend)
        d.connect(legend,"brushing",scatter,"brushing")
    
    for colourMap in ContinuousPalette.listColourMaps():
        palette = ContinuousPalette(colourMap=colourMap) 
        scatter = Scatter(scatterdata1, 400, 400, palette)
        d.add(Text(colourMap,font_height=32))
        d.add(scatter)
        legend = Legend(palette,400,legend_columns=2)
        d.add(legend)
        # d.connect(legend,"brushing",bar,"brushing")
    
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()
