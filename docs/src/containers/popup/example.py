# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.containers import Map, Popup
from visigoth.utils.mapping import Geocoder, Mapping, Projections
from visigoth.map_layers import WMTS, Geoplot
from visigoth.map_layers.geoplot import Multipoint
from visigoth.common import Space

d = Diagram()

gc = Geocoder()

center = gc.fetchCenter("New York")
bounds = Mapping.computeBoundaries(center,200000,projection=Projections.EPSG_3857)

timesq = gc.fetchCenter("Times Square, New York")
timesq_bounds = Mapping.computeBoundaries(timesq,500,projection=Projections.EPSG_3857)

timesq_m = Map(256,boundaries=timesq_bounds,projection=Projections.EPSG_3857,font_height=5)
timesq_wms = WMTS()
timesq_m.add(timesq_wms)
timesq_popup = Popup(timesq_m,"Times Square",fill="white")

m = Map(512,boundaries=bounds,projection=Projections.EPSG_3857,zoom_to=2)

wms = WMTS()
wms.setInfo("Map")

gp = Geoplot(multipoints=[Multipoint([timesq],label="Times Square",popup=timesq_popup)])

m.add(wms)
m.add(gp)
d.add(Space(100))
d.add(m)

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()



