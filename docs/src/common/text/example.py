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

from visigoth.common import Text, Span
from visigoth.containers import Box

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    d = Diagram(fill="white",title="visigoth Text example",description="some description")
    d.setFontEmbedding(True)

    d.add(Box(Text("Some Small Text",font_height=10)))
    d.add(Box(Text("Link to repo",url="https://github.com/visigoths/visigoth")))
    d.add(Box(Text("Some Fancy Text",font_height=32,text_attributes={"stroke":"darkblue", "fill":"red"})))
    d.add(Box(Text("Some Big Text",font_height=48)))
    d.add(Box(Text("Difffferent",text_attributes={"font-family":"Raleway"})))
    d.add(Box(Text(
        [Span("Text can be combined with"),
         Span(" a url",url="https://github.com/visigoths/visigoth"),
         Span(" different styles",text_attributes={"font-style":"normal"}),
         Span(" different fonts", text_attributes={"font-family":"Roboto"}),
         Span(" different sizes ",font_height=32),
         Span(" and different colours!", text_attributes={"stroke":"red"})],max_width=400,font_height=24)))

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()




