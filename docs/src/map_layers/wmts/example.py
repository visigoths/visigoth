# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import WMTS, Geoplot
from visigoth.utils.mapping import Projections
from visigoth.map_layers.geoplot import Multipoint

d = Diagram()

bounds = ((166.509144322, -46.641235447),(178.517093541, -34.4506617165))

m1 = Map(512,boundaries=bounds,zoom_to=2,projection=Projections.EPSG_3857)
m1.add(WMTS())
m1.add(Geoplot(multipoints=[Multipoint([(172.639847,-43.525650)],label="Christchurch",marker=True,fill="#FF000050")]))
d.add(Box(m1))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

