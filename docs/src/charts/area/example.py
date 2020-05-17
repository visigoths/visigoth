# -*- coding: utf-8 -*-

from visigoth.diagram import Diagram
from visigoth.charts.area import Area
from visigoth.common.legend import Legend

data = [(0,1,"A"),(1,1.5,"A"),(2,1.6,"A"),(3,1.3,"A"),(4,1.2,"A")] + \
    [(0,4,"B"),(1,3.5,"B"),(2,2.6,"B"),(3,1.6,"B"),(4,0.8,"B")] + \
    [(0,1,"C"),(1,1.7,"C"),(2,2.6,"C"),(3,2.8,"C"),(4,3.1,"C")]

d = Diagram(fill="white")

a = Area(data,width=500,height=400)

d.add(a)
legend = Legend(a.getPalette(),width=400,legend_columns=2)
d.add(legend)

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

