# -*- coding: utf-8 -*-

from visigoth.diagram import Diagram
from visigoth.charts.bar import Bar
from visigoth.utils.colour import DiscretePalette
from visigoth.common.legend import Legend

palette = DiscretePalette()

data = [{"c1":"A","c2":10},{"c1":"B","c2":5},{"c1":"C","c2":6},{"c1":"D","c2":8}]

d = Diagram()

bar1 = Bar(data,x="c1",y="c2",colour="c1",width=400, height=400, palette=palette,labelfn=lambda k,v:"%d"%v)
d.add(bar1)
legend = Legend(palette,400,legend_columns=2)
d.add(legend)

d.connect(bar1,"colour",legend,"colour")
d.connect(legend,"colour",bar1,"colour")

html = d.draw(format="html")
f = open("example.html", "w")
f.write(html)
f.close()

