# -*- coding: utf-8 -*-

import csv

from visigoth import Diagram
from visigoth.charts import SOM
from visigoth.common import Text, Legend
from visigoth.utils.colour import ContinuousColourManager


ccolour_manager0 = ContinuousColourManager(withIntervals=False)

ccolour_manager1 = ContinuousColourManager(withIntervals=False)

ccolour_manager2 = ContinuousColourManager(withIntervals=False)

ccolour_manager3 = ContinuousColourManager(withIntervals=False)

min_temp_data = []
max_temp_data = []
precipitation_data = []
snowfall_data = []
reader = csv.reader(open("climate_by_city.csv"))
headers_read = False
for line in reader:
    if not headers_read:
        headers_read = True
    else:
        label = line[0]
        cat = ""
        values = list(map(lambda s:float(s),line[1:]))
        min_temp_data.append((label,cat,values[0:12]))
        max_temp_data.append((label,cat,values[12:24]))
        precipitation_data.append((label,cat,values[24:36]))
        snowfall_data.append((label,cat,values[36:48]))

def mean(vec):
    return sum(vec)/len(vec)

d = Diagram(fill="white")

som0 = SOM(min_temp_data,512,dimension=lambda l: mean(l),dimensionPalette=ccolour_manager0)
som1 = SOM(max_temp_data,512,dimension=lambda l: mean(l),dimensionPalette=ccolour_manager1)
som2 = SOM(precipitation_data,512,dimension=lambda l: mean(l),dimensionPalette=ccolour_manager2)
som2.getPalette().setDefaultColour("white")

d.add(Text("Cities clustered by monthly minimum temperature(s)"))
d.add(som0)
d.add(Text("Mean minimum daily temperature (Celsius)",font_height=12))
d.add(Legend(ccolour_manager0,width=500))

d.add(Text("Cities clustered by monthly maximum temperature(s)"))
d.add(som1)
d.add(Text("Mean maximum daily temperature (Celsius)",font_height=12))
d.add(Legend(ccolour_manager1,width=500))

d.add(Text("Cities clustered by precipitation"))
d.add(som2)
d.add(Text("Mean daily precipitation (mm)",font_height=12))
d.add(Legend(ccolour_manager2,width=500))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

