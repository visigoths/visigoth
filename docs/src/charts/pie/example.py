# -*- coding: utf-8 -*-

from visigoth.diagram import Diagram
from visigoth.charts import Pie
from visigoth.utils.colour import DiscretePalette
from visigoth.common import Legend

palette = DiscretePalette()
    
data = [("A",10),("B",4),("D",12),("D.2",3),("D.3",5)]

d = Diagram()

pie = Pie(data,colour=0,value=1,width=400, height=400, palette=palette, doughnut=True)
d.add(pie)
legend = Legend(palette,400,legend_columns=2)
d.add(legend)
d.connect(legend,"colour",pie,"colour")
d.connect(pie,"colour",legend,"colour")
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

