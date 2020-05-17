# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.containers import Box
from visigoth.common import Text

d = Diagram()
d.add(Text("Some Text"))
d.add(Box(Text("Some Text in an Orange Box"),fill="orange",stroke="darkred",stroke_width=4,margin=10,padding=5))

html = d.draw(format="html")
f = open("example.html", "w")
f.write(html)
f.close()

