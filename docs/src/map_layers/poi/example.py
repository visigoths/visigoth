# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.common import Space
from visigoth.map_layers import WMS, POI

data = [{"id": "1094594877923491840", "lon": -0.28002518, "lat": 51.55696202},
    {"id": "1094595003945488384", "lon": -0.11993334, "lat": 51.53098437},
    {"id": "1094595017631514624", "lon": -0.12731805, "lat": 51.50711486},
    {"id": "1094595262889291777", "lon": -0.48618965, "lat": 51.4718463},
    {"id": "1094595309081116672", "lon": -0.126, "lat": 51.551},
    {"id": "1094595530804449280", "lon": -0.1317595, "lat": 51.50830388},
    {"id": "1094595627860746241", "lon": -0.12731805, "lat": 51.50711486},
    {"id": "1094596872352624640", "lon": -0.12731805, "lat": 51.50711486}]

d = Diagram(margin_left=200,margin_right=200)
poi = POI(data,lon="lon",lat="lat",tweet="id")

m1 = Map(512,width_to_height=1)
m1.addLayer(WMS(type="osm"))
m1.addLayer(poi)
d.add(Space(100))
d.add(Box(m1))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

