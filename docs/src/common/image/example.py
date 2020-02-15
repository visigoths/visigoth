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

import os
import sys
import argparse

from visigoth.diagram import Diagram
from visigoth.common import Image
from visigoth.common import Text

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    folder = os.path.split(sys.argv[0])[0]

    d = Diagram(fill="white")
    d.add(Image(mime_type="image/jpeg",content_bytes=open(os.path.join(folder,"MtCleveland.jpg"),"rb").read(),tooltip="MtCleveland Volcano Eruption"))
    d.add(Image(scale=2.0,path_or_url=os.path.join(folder,"MtCleveland.png"),tooltip="MtCleveland Volcano Eruption"))
    d.add(Image(scale=0.5,mime_type="image/gif",content_bytes=open(os.path.join(folder,"MtCleveland.gif"),"rb").read(),tooltip="MtCleveland Volcano Eruption"))
    # d.add(Image(path_or_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/4a/MtCleveland_ISS013-E-24184.jpg/320px-MtCleveland_ISS013-E-24184.jpg",tooltip="MtCleveland Volcano Eruption"))
    d.add(Text("Attribution: Public Domain",url="https://en.wikipedia.org/wiki/Volcano#/media/File:MtCleveland_ISS013-E-24184.jpg",font_height=18))
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()
