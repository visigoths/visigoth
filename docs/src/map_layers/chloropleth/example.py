# -*- coding: utf-8 -*-

import random

from visigoth.diagram import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers.chloropleth import Chloropleth
from visigoth.common import Text, Space, Legend
from visigoth.utils.colour import ContinuousPalette
import os.path

palette = ContinuousPalette()
palette.addColour("green",0.0).addColour("blue",10.0)

rng = random.Random()
d = Diagram(fill="white")

path = os.path.join(os.path.split(__file__)[0],"aus_state.geojson")
d.add(Text("randomness",font_height=50,text_attributes={"stroke":"purple"}))
d.add(Space(20,20))
c = Chloropleth(path,lambda props:rng.random()*10,"STATE_NAME",palette)
m = Map(512,zoom_to=4)
m.addLayer(c)
d.add(Box(m))
d.add(Space(20,20))
d.add(Legend(palette,width=500,legend_columns=3))
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

