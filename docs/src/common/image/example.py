# -*- coding: utf-8 -*-

import os
import sys

from visigoth import Diagram
from visigoth.common import Image, Text

folder = os.path.split(sys.argv[0])[0]

d = Diagram(fill="white")
d.add(Image(mime_type="image/jpeg",content_bytes=open(os.path.join(folder,"MtCleveland.jpg"),"rb").read(),
            tooltip="MtCleveland Volcano Eruption"))
d.add(Image(scale=2.0,path_or_url=os.path.join(folder,"MtCleveland.png"),
            tooltip="MtCleveland Volcano Eruption"))
d.add(Image(scale=0.5,mime_type="image/gif",content_bytes=open(os.path.join(folder,"MtCleveland.gif"),"rb").read(),
            tooltip="MtCleveland Volcano Eruption"))
d.add(Text("Attribution: Public Domain",url="https://en.wikipedia.org/wiki/Volcano#/media/File:MtCleveland_ISS013-E-24184.jpg",font_height=18))
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()
