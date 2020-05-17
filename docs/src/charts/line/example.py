# -*- coding: utf-8 -*-

import random
import datetime

from visigoth import Diagram
from visigoth.charts import Line
from visigoth.containers import Box
from visigoth.common import Legend

r = random.Random()
data = []
y = -0.05
for cat in ["A","B","C","D"]:
    for idx in range(36):
        data.append((datetime.datetime(2018,1,1,0,idx,0),y+r.random()/10,cat))
    y += 0.1

d = Diagram()

al = Line(data,x=0,y=1,colour=2,width=600,height=600)
(ax,ay) = al.getAxes()
ax.setLabel("X axis")
ay.setLabel("Y axis")

d.add(Box(al))

legend = Legend(al.getPalette(),400,legend_columns=2, stroke_width=5)
legend.setDiscreteMarkerStyle("line")
d.add(legend)
d.connect(legend,"colour",al,"colour")
d.connect(al,"colour",legend,"colour")

html = d.draw(format="html",html_title="Visigoth - Line Chart Example")

f = open("example.html", "w")
f.write(html)
f.close()
