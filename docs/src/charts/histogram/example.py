# -*- coding: utf-8 -*-

import random

from visigoth.diagram import Diagram
from visigoth.charts import Histogram
from visigoth.common.legend import Legend

r = random.Random()

data = []
for idx in range(0, 200):
    data.append({"value":r.gauss(1,0.2),"category":"one"})

for idx in range(0, 100):
    data.append({"value":r.gauss(2,0.4),"category":"two"})

d = Diagram()

histogram = Histogram(data,x="value",colour="category")
histogram.getPalette().setOpacity(0.5)
legend = Legend(histogram.getPalette(), width=300)

d.add(histogram)
d.add(legend)

d.connect(legend,"colour",histogram,"colour")
d.connect(histogram,"colour",legend,"colour")

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

