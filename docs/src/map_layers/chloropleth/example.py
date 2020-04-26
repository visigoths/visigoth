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
import random

from visigoth.diagram import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers.chloropleth import Chloropleth
from visigoth.common import Text, Space, Legend
from visigoth.utils.colour import ContinuousPalette
import os.path

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    palette = ContinuousPalette()
    palette.addColour("green",0.0).addColour("blue",10.0)

    rng = random.Random()
    d = Diagram(fill="white")

    path = os.path.join(os.path.split(__file__)[0],"aus_state.geojson")
    d.add(Text("randomness",font_height=50,text_attributes={"stroke":"purple"}))
    d.add(Space(20,20))
    c = Chloropleth(path,lambda props:rng.random()*10,"STATE_NAME",palette)
    m = Map(512,zoom_to=4)
    m.addLayer(c)
    d.add(Box(m))
    d.add(Space(20,20))
    d.add(Legend(palette,width=500,legend_columns=3))
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

