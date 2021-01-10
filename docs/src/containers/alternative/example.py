# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.containers import Alternative, Box, Sequence
from visigoth.charts import Pie, Bar
from visigoth.common import Button, ButtonGrid, Legend
from visigoth.utils.colour import DiscreteColourManager

d = Diagram()

colour_manager0 = DiscreteColourManager()
colour_manager0.addColour("A","#E7FFAC").addColour("B","#FFC9DE")
colour_manager0.addColour("C","#B28DFF").addColour("D","#ACE7FF")

legend = Legend(colour_manager0,legend_columns=2)

data0 = [("A",1.2),("B",0.7),("C",0.4),("D",0.5)]

bar0 = Bar(data0, x=0, y=1, colour=0, width=400, height=400, colour_manager=colour_manager0,labelfn=lambda k,v:"%0.2f"%v)
pie0 = Pie(data0, colour=0, value=1, width=400, height=400, colour_manager=colour_manager0)

a = Alternative()
a.add(pie0)
a.add(bar0)

seq0 = Sequence(orientation="horizontal")
b1 = Button(text="pie chart",click_value=pie0.getId())
b2 = Button(text="bar chart",click_value=bar0.getId())

bg = ButtonGrid()
bg.addButton(0,0,b1,initially_selected=True)
bg.addButton(0,1,b2)

d.add(bg)

d.add(Box(a,fill="lightgrey"))
d.add(legend)
d.connect(bg,"click",a,"show")
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()