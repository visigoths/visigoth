# visigoth

python3 library for plotting data-driven maps with SVG

### Documentation

[API Documentation](http://visigoth.org/index.html)

### Install from PYPI:

```
python3 -m pip install visigoth
```

### Manual Install onto PYTHONPATH:

```
git clone https://github.com/visualtopology/visigoth.git
export PYTHONPATH=$PYTHONPATH:`pwd`/visigoth
```

### Run unit tests

```
# clone repo and configure PYTHONPATH as above
cd visigoth
mkdir tmp_test_results
cd tmp_test_results
python3 -m unittest discover ../tests
# tests will write svg files to the current directory
```

### Quick Simple Map Example:


![Basic Map with OSM/WMS](http://visigoth.org/_static/src/example.svg)

```
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
svg = d.draw(format="svg")

f = open("example.html", "w")
f.write(html)
f.close()

f = open("example.svg","w")
f.write(svg)
f.close()
```



