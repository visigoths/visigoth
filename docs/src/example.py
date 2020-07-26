# -*- coding: utf-8 -*-

import os

from visigoth import Diagram
from visigoth.utils.mapping import Geocoder, Mapping
from visigoth.map_layers import WMS, Geoplot
from visigoth.map_layers.geoplot import Multipoint
from visigoth.containers import Map, Box
from visigoth.common import Text

folder=os.path.split(__file__)[0]

d = Diagram()

# lets see where "HelloWorld" geocodes to!
gc = Geocoder()
center = gc.fetchCenter("Hello World")
bounds = Mapping.computeBoundaries(center,4000)

# create a map with the default projection system (web mercator)
m = Map(768,boundaries=bounds)

# create a base layer with openstreetmap
wms = WMS("osm")
wms.setInfo("Map")

# create a layer with a marker for "HelloWorld"
gps = Geoplot(multipoints=[Multipoint([center],label="Hello World",tooltip="Hello World")])

m.add(wms)
m.add(gps)

# compose the diagram
d.add(Text("Where does \"Hello World\" Geolocate to?",font_height=18))
d.add(Box(m))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

