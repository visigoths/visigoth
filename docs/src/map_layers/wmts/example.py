# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.common import LayerController
from visigoth.map_layers import WMTS, Geoplot
from visigoth.utils.mapping import Projections
from visigoth.map_layers.geoplot import Multipoint

d = Diagram()

bounds = ((166.509144322, -46.641235447),(178.517093541, -34.4506617165))

m1 = Map(512,boundaries=bounds,zoom_to=6,projection=Projections.EPSG_3857)

layers = []
osm = WMTS(embed_images=False)
# https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/1.0.0/WMTSCapabilities.xml

attribution="NASA GIBS"
attribution_url="https://wiki.earthdata.nasa.gov/display/GIBS"

black_marble = WMTS(url="https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/VIIRS_Black_Marble/default/default/GoogleMapsCompatible_Level8/{z}/{y}/{x}.png",embed_images=False,attribution=attribution,attribution_link=attribution_url)
night_lights = WMTS(url="https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/VIIRS_Night_Lights/default/default/GoogleMapsCompatible_Level8/{z}/{y}/{x}.png",embed_images=False,attribution=attribution,attribution_link=attribution_url)
blue_marble = WMTS(url="https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/BlueMarble_NextGeneration/default/GoogleMapsCompatible_Level8/{z}/{y}/{x}.jpeg",embed_images=False,attribution=attribution,attribution_link=attribution_url)
dem1 = WMTS(url="https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/ASTER_GDEM_Color_Index/default/GoogleMapsCompatible_Level12/{z}/{y}/{x}.png",embed_images=False,attribution=attribution,attribution_link=attribution_url)
dem2 = WMTS(url="https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/ASTER_GDEM_Greyscale_Shaded_Relief/default/GoogleMapsCompatible_Level12/{z}/{y}/{x}.jpg",embed_images=False,attribution=attribution,attribution_link=attribution_url)

m1.add(osm)
layers.append({"layer":osm,"label":"OSM"})

m1.add(night_lights)
layers.append({"layer":night_lights,"label":"VIIRS Night Lights"})

m1.add(black_marble)
layers.append({"layer":black_marble,"label":"VIIRS Black Marble"})

m1.add(blue_marble)
layers.append({"layer":blue_marble,"label":"Blue Marble NG"})

m1.add(dem1)
layers.append({"layer":dem1,"label":"Digital Elevation Model 1"})

m1.add(dem2)
layers.append({"layer":dem2,"label":"Digital Elevation Model 2"})


m1.add(Geoplot(multipoints=[Multipoint([(172.639847,-43.525650)],label="Christchurch",marker=True,fill="#FF000050")]))
d.add(Box(m1))

mlm = LayerController(layers,title="Layers",height=600,width=400)
d.connect(mlm,"manage_layers",m1,"manage_layers")
d.add(mlm)

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

