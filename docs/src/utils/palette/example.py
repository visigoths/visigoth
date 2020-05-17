# -*- coding: utf-8 -*-

import random

from visigoth.diagram import Diagram
from visigoth.charts import Scatter
from visigoth.utils.colour import DiscretePalette, ContinuousPalette
from visigoth.common import Text, Legend

rng = random.Random()
scatterdata1 = [(rng.random(),rng.random(),"",10*rng.random(),10) for x in range(0,50)]
scatterdata2 = [(rng.random(),rng.random(),"",rng.choice(["A","B","C","D","E","F"]),10) for x in range(0,50)]

d = Diagram(fill="white")

for colourMap in DiscretePalette.listColourMaps():
    palette = DiscretePalette(colourMap=colourMap)
    scatter = Scatter(scatterdata2, 400, 400, palette)
    d.add(Text(colourMap,font_height=32))
    d.add(scatter)
    legend = Legend(palette,400)
    d.add(legend)
    d.connect(legend,"colour",scatter,"colour")

for colourMap in ContinuousPalette.listColourMaps():
    palette = ContinuousPalette(colourMap=colourMap)
    scatter = Scatter(scatterdata1, 400, 400, palette)
    d.add(Text(colourMap,font_height=32))
    d.add(scatter)
    legend = Legend(palette,400,legend_columns=2)
    d.add(legend)

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

