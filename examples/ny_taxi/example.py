# -*- coding: utf-8 -*-

import csv
import os.path
import gzip

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import WMTS, Hexbin
from visigoth.common import Text, MapLayerManager, Legend
from visigoth.utils.colour import ContinuousPalette
from visigoth.utils.mapping import Projections

bounds = ((-74.2, 40.6), (-73.5, 40.9))


lon_min = bounds[0][0]
lat_min = bounds[0][1]
lon_max = bounds[1][0]
lat_max = bounds[1][1]

data = []
freqs_by_hour = {h:0 for h in range(24)}

headers = {}

# load the data from CSV
f = gzip.open(os.path.join(os.path.split(__file__)[0],"pickup_dropoff_2015-01-01.csv.gz"),"rt")
rdr = csv.reader(f)

for row in rdr:
    if not headers:
        for idx in range(len(row)):
            headers[row[idx]] = idx
    else:
        data.append((float(row[headers["lon"]]),float(row[headers["lat"]])))
f.close()

d = Diagram(fill="white")

# create the map and and an open street map base layer
m = Map(1024,bounds,projection=Projections.EPSG_3857,zoom_to=8)
wms = WMTS(embed_images=False)
wms.setInfo("Map")
m.add(wms)

palette = ContinuousPalette(colourMap="viridis",withIntervals=False)

# define the heatmap
heatmap = Hexbin(data,palette=palette,nr_bins_across=400,stroke_width=0,stroke="none",min_freq=1)
m.add(heatmap)

# lay out the diagram, starting with a title
d.add(Text("NY Yellow Cab pickup/dropoff locations"))

# add the legend and map
d.add(Box(m))
d.add(Legend(palette,label="Frequency (thousands)",labelfn=lambda x:str(int(x/1000))))

# add a layer manager to allow layers to be turned on and off
mlm = MapLayerManager([{"layer":heatmap,"label":"Trips"}],title="Select Layer(s)",height=150)
d.add(mlm)
d.connect(mlm,"manage_layers",m,"manage_layers")
d.add(Text("NY Taxi Trips"))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()
