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

d.add(Text("GDP vs Life Expectancy, Selected Countries, 1952 - 2007"))
s = Scatter(datapoints,x="lifeExp",y="gdpPercap",slice="year",size="pop",colour="country",label="country",width=800)
(ax,ay) = s.getAxes()
ay.setMaxValue(60000)
ay.setMinValue(0)
sm = SliceController(title="Year",width=800)
d.add(s)
d.add(sm)
d.connect(sm,"slice",s,"slice")
d.add(Text("Data source: https://www.gapminder.org/",font_height=12))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()