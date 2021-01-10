# -*- coding: utf-8 -*-

import random
import csv

from visigoth.diagram import Diagram
from visigoth.common import Text, Space, Legend
from visigoth.containers import Grid
from visigoth.charts import Scatter
from visigoth.utils.colour import DiscreteColourManager
from visigoth.utils.marker.marker_manager import MarkerManager

rng = random.Random()
d = Diagram(fill="white")

data = []
reader = csv.reader(open("iris.csv"))
keys = {}
data = []
for line in reader:
    if not keys:
        for idx in range(0,len(line)):
            keys[line[idx]] = idx
    else:
        data.append({k:line[keys[k]] for k in keys})

p = DiscreteColourManager()
g = Grid()

fields = ["sepal_length","sepal_width","petal_length","petal_width"]

mm = MarkerManager(default_radius=2)

def createPlot(x_field,y_field,data,colour_manager):
    sdata = [(float(row[x_field]),float(row[y_field]),row["species"]) for row in data]
    sp = Scatter(sdata, colour=2, width=250, height=250, colour_manager=colour_manager, font_height=14)
    (ax,ay) = sp.getAxes()
    ax.setLabel(x_field)
    ay.setLabel(y_field)
    return sp

l = Legend(p,width=800,legend_columns=3)

for r in range(len(fields)):
    for c in range(len(fields)):
        x_field = fields[r]
        y_field = fields[c]
        if x_field == y_field:
            e = Text(x_field)
        else:
            e = createPlot(x_field,y_field,data,p)
            d.connect(l,"colour",e,"colour")
        g.add(r,c,e)

d.add(g)
d.add(l)
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

