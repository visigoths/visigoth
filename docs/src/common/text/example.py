# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.common import Text, Span
from visigoth.containers import Box

d = Diagram(fill="white",title="visigoth Text example",description="some description")
d.setFontEmbedding(True)

d.add(Box(Text("Some Small Text",font_height=10)))
d.add(Box(Text("Link to repo",url="https://github.com/visigoths/visigoth")))
d.add(Box(Text("Some Fancy Text",font_height=32,text_attributes={"stroke":"darkblue", "fill":"red"})))
d.add(Box(Text("Some Big Text",font_height=48)))
d.add(Box(Text("Different",text_attributes={"font-family":"Raleway"})))
d.add(Box(Text(
    [Span("Text can be combined with"),
     Span(" a url",url="https://github.com/visigoths/visigoth"),
     Span(" different styles",text_attributes={"font-style":"normal"}),
     Span(" different fonts", text_attributes={"font-family":"Roboto"}),
     Span(" different sizes ",font_height=32),
     Span(" and different colours!", text_attributes={"stroke":"red"})],max_width=400,font_height=24)))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()




