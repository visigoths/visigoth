# -*- coding: utf-8 -*-

import random

from visigoth.diagram import Diagram
from visigoth.charts import Scatter
from visigoth.utils.colour import DiscreteColourManager, ContinuousColourManager
from visigoth.common import Text, Legend

rng = random.Random()
scatterdata1 = [(rng.random(),rng.random(),"",10*rng.random(),10) for x in range(0,50)]
scatterdata2 = [(rng.random(),rng.random(),"",rng.choice(["A","B","C","D","E","F"]),10) for x in range(0,50)]

d = Diagram(fill="white")

for colourMap in DiscreteColourManager.listColourMaps():
    colour_manager = DiscreteColourManager(colourMap=colourMap)
    scatter = Scatter(scatterdata2, 400, 400, colour_manager)
    d.add(Text(colourMap,font_height=32))
    d.add(scatter)
    legend = Legend(colour_manager,400)
    d.add(legend)
    d.connect(legend,"colour",scatter,"colour")

for colourMap in ContinuousColourManager.listColourMaps():
    colour_manager = ContinuousColourManager(colourMap=colourMap)
    scatter = Scatter(scatterdata1, 400, 400, colour_manager)
    d.add(Text(colourMap,font_height=32))
    d.add(scatter)
    legend = Legend(colour_manager,400,legend_columns=2)
    d.add(legend)

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

