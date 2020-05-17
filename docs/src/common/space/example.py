# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.common import Space, Text

d = Diagram(fill="white")
d.add(Text("Example Space, see below...",font_height=32,text_attributes={"stroke":"darkblue"}))
d.add(Space(200,200))
d.add(Text("...did you miss it? ^^^^",font_height=32,text_attributes={"stroke":"darkblue"}))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

