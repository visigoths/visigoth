# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.containers import Sequence, Box
from visigoth.common import Text, Space

d = Diagram()

s0 = Sequence()
s0.add(Space(0,300))
s0.add(Text("Left").setLeftJustified()).add(Text("Center")).add(Text("Right").setRightJustified())
d.add(s0)

s = Sequence(spacing=20,orientation="horizontal")
s.add(Box(Text("Red Box"),fill="red")).add(Box(Text("Green Box"),fill="green")).add(Box(Text("Blue Box"),fill="blue"))
d.add(Box(s,fill="lightgrey"))

html = d.draw(format="html")
f = open("example.html", "w")
f.write(html)
f.close()

