# -*- coding: utf-8 -*-

import os
import sys

from visigoth import Diagram
from visigoth.common import Button
from visigoth.common import Image

d = Diagram()
d.setDefaultTextAttributes({"font-weight":"bold"})

folder = os.path.split(sys.argv[0])[0]
content_bytes=open(os.path.join(folder,"..","image","MtCleveland.jpg"),"rb").read()
i = Image(mime_type="image/jpeg",
          content_bytes=content_bytes,
          tooltip="MtCleveland Volcano Eruption")
d.add(Button(text="Link",image=i,fill="orange",stroke="blue",padding=10))
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()
