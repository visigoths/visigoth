# -*- coding: utf-8 -*-

import random

from visigoth.diagram import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers.chloropleth import Chloropleth
from visigoth.common import Text, Space, Legend
from visigoth.utils.colour import ContinuousPalette
import os.path

palette = ContinuousPalette()

rng = random.Random()
d = Diagram(fill="white")

path = os.path.join(os.path.split(__file__)[0],"aus_state.geojson")

c = Chloropleth(path,lambda props:int(props["STATE_CODE"]),None,palette)
m = Map(512,zoom_to=4)
m.add(c)
d.add(Box(m))
d.add(Legend(palette,width=500,font_height=10))
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

