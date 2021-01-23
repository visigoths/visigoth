# -*- coding: utf-8 -*-

from visigoth.diagram import Diagram
from visigoth.charts import Pie
from visigoth.utils.colour import DiscreteColourManager
from visigoth.common import Legend

colour_manager = DiscreteColourManager()
    
data = [("A","",10),("B","",4),("D","",0),("D","D.1",1),("D","D.2",20),("D","D.3",5)]

d = Diagram()

pie = Pie(data,colour=[0,1],value=2,width=400, height=400, colour_manager=colour_manager, doughnut=True)
d.add(pie)
legend = Legend(colour_manager,400,legend_columns=2)
d.add(legend)
d.connect(legend,"colour",pie,"colour")
d.connect(pie,"colour",legend,"colour")
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

