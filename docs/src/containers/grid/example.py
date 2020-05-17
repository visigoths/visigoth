# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.containers import Grid
from visigoth.common import Text

d = Diagram()

d.add(Text("Simple Grid"))

g = Grid()
g.add(0,0,Text("Top-Left Cell in Grid"))
g.add(1,0,Text("Bottom-Left").setRightJustified())
g.add(0,1,Text("Top-Right").setLeftJustified())
g.add(1,1,Text("Bottom-Right Cell in Grid"))
d.add(g)

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

