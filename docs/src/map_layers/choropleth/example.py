# -*- coding: utf-8 -*-

import random

from visigoth.diagram import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers.choropleth import Choropleth
from visigoth.common import Text, Space, Legend
from visigoth.utils.colour import ContinuousColourManager
import os.path

colour_manager = ContinuousColourManager()

rng = random.Random()
d = Diagram(fill="white")

path = os.path.join(os.path.split(__file__)[0],"aus_state.geojson")

c = Choropleth(path, lambda props:int(props["STATE_CODE"]), None, colour_manager)
m = Map(512,zoom_to=4)
m.add(c)
d.add(Box(m))
d.add(Legend(colour_manager,width=500,font_height=10))
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

