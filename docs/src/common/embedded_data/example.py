# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.common import EmbeddedData

data = [("A",10),("B",4),("D",12),("D.2",3),("D.3",5)]*100

d = Diagram()

eh1 = EmbeddedData(data,"Download data as a zipped CSV",filename="data.csv",
                   column_labels={0:"LETTER",1:"NUMBER"})
d.add(eh1)

eh2 = EmbeddedData(data,"Download data as CSV",filename="data.csv",zip=False,
                   column_labels={0:"LETTER",1:"NUMBER"})
d.add(eh2)

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()