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

import os
import sys
import argparse

from visigoth.diagram import Diagram
from visigoth.common import Button
from visigoth.common import Image

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    d = Diagram(fill="white")
    d.setDefaultTextAttributes({"font-weight":"bold"})

    folder = os.path.split(sys.argv[0])[0]

    i = Image(mime_type="image/jpeg",content_bytes=open(os.path.join(folder,"..","image","MtCleveland.jpg"),"rb").read(),tooltip="MtCleveland Volcano Eruption")

    d.add(Button(text="Link",image=i,fill="orange",stroke="blue",padding=10))
    
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()
