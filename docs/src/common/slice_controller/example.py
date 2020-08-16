# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.common import SliceController, Legend
from visigoth.charts import Scatter

import random

rng = random.Random()

items = [
    { "x":10*rng.random(), "y":10*rng.random(), "c":rng.choice(["A","B","C"]),
      "sz":10*rng.random(), "dx":rng.random()-0.5, "dy":rng.random()-0.5, "dsize":rng.random()-0.5 } for i in range(0,10)]

datapoints = [
    { "iteration":iter, "x":i["x"]+iter*i["dx"], "y":i["y"]+iter*i["dy"], "c":i["c"], "sz":i["sz"]+iter*i["dsize"] } for i in items for iter in range(20)
]
d = Diagram()

s = Scatter(width=512,height=512,data=datapoints,x="x",y="y",slice="iteration",size="sz",colour="c",label="c")
(ax,ay) = s.getAxes()

leg = Legend(s.getPalette(),512)
sm = SliceController(title="Iteration",width=384,height=200)
d.add(s)
d.add(sm)
d.add(leg)
d.connect(sm,"slice",s,"slice")
d.connect(leg,"colour",s,"colour")

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()