# -*- coding: utf-8 -*-

import random

from visigoth.diagram import Diagram
from visigoth.charts import Scatter
from visigoth.utils.colour import DiscreteColourManager
from visigoth.common import Legend

colour_manager = DiscreteColourManager()

r = random.Random()
data = []
for idx in range(0,100):
    data.append((r.random(),r.random(),"p"+str(idx),r.choice(["A","B","C","D"]),r.choice([3,5,9])))

d = Diagram()

scatter = Scatter(data, x=0, y=1, label=2, colour=3, size=4, colour_manager=colour_manager)
(ax,ay) = scatter.getAxes()
ax.setMinValue(0.0).setMaxValue(1.0)
ay.setMinValue(0.0).setMaxValue(1.0)
legend = Legend(colour_manager,400,legend_columns=2)
legend.setDiscreteMarkerStyle("circle")

d.add(legend)
d.connect(legend,"colour",scatter,"colour")
d.connect(scatter,"colour",legend,"colour")

(xaxis,yaxis) = scatter.getAxes()
xaxis.setStroke("red",3)
yaxis.setStroke("blue",3)
d.add(scatter)
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

