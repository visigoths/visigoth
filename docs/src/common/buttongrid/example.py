# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.common import Button, ButtonGrid

d = Diagram()

bg = ButtonGrid()
bg.addButton(0,1,Button("North Button"))
bg.addButton(1,0,Button("West Button"))
bg.addButton(1,1,Button("Centre Button"),initially_selected=True)
bg.addButton(1,2,Button("East Button"))
bg.addButton(2,1,Button("South Button"))

d.add(bg)
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()
