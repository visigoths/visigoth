# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.common import SliceController, Legend, Text
from visigoth.charts import Scatter


import csv
rdr = csv.reader(open("data.csv"))

preprocess = {
    "year":lambda x:int(x) if x else None,
    "gdpPercap": lambda x: float(x) if x else None,
    "pop": lambda x: int(x) if x else None,
    "lifeExp": lambda x: float(x) if x else None,
}

columns = {}
datapoints = []
for row in rdr:
    if not columns:
        for idx in range(len(row)):
            columns[row[idx]] = idx
    else:
        data = {}
        for col in columns:
            data[col] = row[columns[col]]
            if col in preprocess:
                data[col] = preprocess[col](data[col])
        datapoints.append(data)
d = Diagram()

s = Scatter(datapoints,x="lifeExp",y="gdpPercap",slice="year",size="pop",colour="country",label="country")
(ax,ay) = s.getAxes()
ay.setMaxValue(60000)
ay.setMinValue(0)
leg = Legend(s.getPalette(),512)
sm = SliceController(title="Year")
d.add(s)
d.add(sm)
d.add(leg)
d.connect(sm,"slice",s,"slice")
d.connect(leg,"colour",s,"colour")

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()