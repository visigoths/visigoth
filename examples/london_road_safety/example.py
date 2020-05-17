# -*- coding: utf-8 -*-

import csv

from visigoth import Diagram
from visigoth.containers import Map, Box
from visigoth.map_layers import WMS, KDE, Geoplot
from visigoth.map_layers.geoplot import Multipoint
from visigoth.charts import Area
from visigoth.common import Text, MapLayerManager, Legend
from visigoth.utils.colour import DiscretePalette, ContinuousPalette
from visigoth.utils.mapping import Geocoder, Mapping, Projections

# get the boundaries of a region approximately 20 km radius around Central London

gc = Geocoder()
center = gc.fetchCenter("London")
bounds = Mapping.computeBoundaries(center,20000)

lon_min = bounds[0][0]
lat_min = bounds[0][1]
lon_max = bounds[1][0]
lat_max = bounds[1][1]

data = []
freqs_by_hour = {h:0 for h in range(24)}

headers = {}

# load the data from CSV
rdr = csv.reader(open("dftRoadSafetyData_Accidents_2018.csv","r"))

for row in rdr:
    if not headers:
        for idx in range(len(row)):
            headers[row[idx]] = idx
    else:
        try:
            lat = float(row[headers["Latitude"]])
            lon = float(row[headers["Longitude"]])
            hour = int(row[headers["Time"]][:2])
        except:
            continue # some records do not have an hour, lat and lon
        severity = int(row[headers["Accident_Severity"]])

        # ignore accidents that occur outside the london area or are not serious
        if lon >= lon_min and lon <= lon_max \
                and lat >= lat_min and lat <= lat_max \
                and (severity == 1 or severity == 2):
            category = "fatal"
            if severity == 2:
                category = "serious"
            data.append((lon,lat,category))
            freqs_by_hour[hour] = 1+freqs_by_hour[hour]

# compute some summary stats - totals for each type of accident
total_fatal = len([1 for (_,_,cat) in data if cat == "fatal" ])
total_serious = len([1 for (_,_,cat) in data if cat == "serious" ])

d = Diagram(fill="white")

# create the map and and an open street map base layer
m = Map(768,bounds,projection=Projections.ESPG_3857,zoom_to=2)
wms = WMS("osm")
wms.setInfo("Map")
m.addLayer(wms)

# define a palette for the heatmap ranging from white to blue to red
palette = ContinuousPalette()
palette.addColour("#FFFFFF",0).addColour("#0000FF",1).addColour("#FF0000",2)

# define the heatmap
heatmap = KDE([(lon,lat) for (lon,lat,_) in data],bandwidth=300,nr_samples_across=100,palette=palette,label_fn=None)
heatmap.setOpacity(0.5)
m.addLayer(heatmap)

# define a layer plotting a point at the location of each accident
mp1 = Multipoint([(lon,lat) for (lon,lat,cat) in data if cat == "fatal"],fill="red",marker=False,radius=8)
mp2 = Multipoint([(lon,lat) for (lon,lat,cat) in data if cat == "serious"],fill="grey",marker=False,radius=3)
gp = Geoplot(multipoints=[mp1,mp2])
gp.setInfo("UK Department for Transport","","UK Department for Transport","http://data.dft.gov.uk/road-accidents-safety-data/dftRoadSafetyData_Accidents_2018.csv")
gp.setVisible(False) # hide this layer by default
m.addLayer(gp)

# add area chart showing the distribution of all accidents
area_palette = DiscretePalette()
area_palette.setDefaultColour("lightblue")
area_data = []
for hour in freqs_by_hour:
    area_data.append((hour,freqs_by_hour[hour]))
area_chart = Area(area_data, x=0, y=1, colour=None, width=512, height=512, palette=area_palette)
(ax,ay) = area_chart.getAxes()
ax.setLabel("Time Of Day (Hour)")
ay.setLabel("Accident Frequency/Hour")
ax.setTickPositions(list(range(24)))

# lay out the diagram, starting with a title
d.add(Text("London Area Serious and Fatal Road Accidents 2018"))

# define a palette for the accident site plot with totals
discrete_palette = DiscretePalette()
discrete_palette.addCategory("%d Serious Non-Fatal Accidents"%(total_serious), "grey").addCategory("%d Fatal Accidents"%(total_fatal), "red")

# add the legend and map
d.add(Legend(discrete_palette,width=700, legend_columns=2, font_height=18))
d.add(Box(m))

# add a layer manager to allow layers to be turned on and off
mlm = MapLayerManager([{"layer":gp,"label":"Accident Locations"},{"layer":heatmap,"label":"Accident Heatmap"}],title="Select Layer(s)",height=150)
d.add(mlm)
d.connect(mlm,"manage_layers",m,"manage_layers")
d.add(Text("Serious and Fatal Accidents By Time Of Day"))
d.add(area_chart)

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()