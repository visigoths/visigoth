# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import argparse

from visigoth import Diagram

from visigoth.containers import Map, Sequence
from visigoth.utils.mapping import Geocoder, Mapping
from visigoth.map_layers import WMS, Geoimport, Ruler
from visigoth.containers.box import Box
from visigoth.common import Text
from visigoth.common import MapLayerManager
from visigoth.utils.colour import DiscretePalette
from visigoth.common import Legend

from visigoth.utils.mapping import Projections


parser = argparse.ArgumentParser()
parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
args = parser.parse_args()

folder=os.path.split(__file__)[0]

d = Diagram(fill="white")

gc = Geocoder()
center = gc.fetchCenter("London")
bounds = Mapping.computeBoundaries(center,20000)

m = Map(768,boundaries=bounds,projection=Projections.ESPG_3857)
wms = WMS("osm")
wms.setInfo("Map")

m.addLayer(wms)

discrete_palette = DiscretePalette()
discrete_palette.addCategory("Ultra Low Emissions Zone 2019", "red").addCategory("Ultra Low Emissions Zone 2021", "blue")

# downloaded from https://data.cdrc.ac.uk/dataset/4ce01612-cd21-459d-8bcb-6b02c34deb2e/resource/f99f3701-b88a-4806-b673-377032f34a1b/download/londoncongestionchargezone.json
path1 = os.path.join(os.path.split(__file__)[0],"ulez_2019.geojson")
zones1 = Geoimport(path1,polygon_style=lambda p:{"stroke":"red","stroke_width":3,"fill":"#00000030"})
zones1.setInfo("Consumer Data Research Center","","Consumer Data Research Center","https://data.cdrc.ac.uk/dataset/lez")
m.addLayer(zones1)

# downloaded from https://data.cdrc.ac.uk/dataset/4ce01612-cd21-459d-8bcb-6b02c34deb2e/resource/b2641650-a809-421d-8a34-940eb9b5cc8b/download/londonultralowemissionzoneulez2021.geojson
path2 = os.path.join(os.path.split(__file__)[0],"ulez_2021.geojson")
zones2 = Geoimport(path2,polygon_style=lambda p:{"stroke":"blue","stroke_width":3,"fill":"#00000030"})
zones2.setInfo("Consumer Data Research Center","","Consumer Data Research Center","https://data.cdrc.ac.uk/dataset/lez")
m.addLayer(zones2)

m.addLayer(Ruler())

s1 = Sequence()
s1.add(Text("London Ultra Low Emission Zones"))
s1.add(Legend(discrete_palette,width=700, legend_columns=2, font_height=18))
s1.add(Box(m))

s2 = Sequence(orientation="horizontal")
s2.add(s1)
mlm = MapLayerManager([{"layer":zones1,"label":"Ultra Low Emissions Zone 2019"},{"layer":zones2,"label":"Ultra Low Emissions Zone 2021"}],title="Select Emissions Zones",height=150)
s2.add(mlm)

d.add(s2)
d.connect(mlm,"manage_layers",m,"manage_layers")

svg = d.draw()

f = open(args.outpath, "wb")
f.write(svg)
f.close()

