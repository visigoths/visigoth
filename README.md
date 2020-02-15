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
git clone https://github.com/visigoths/visigoth.git
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


![Basic Map with OSM/WMS](http://visigoth.org/src/example.svg)

```
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
from visigoth.containers.map import Map
from visigoth.utils.mapping import Geocoder, Mapping, Projections
from visigoth.map_layers import WMS, Geoplot
from visigoth.map_layers.geoplot import Multipoint
from visigoth.containers import Box
from visigoth.common.text import Text

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    folder=os.path.split(__file__)[0]

    d = Diagram(fill="white")

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

    m.addLayer(wms)
    m.addLayer(gps)

    # compose the diagram
    d.add(Text("Where does \"Hello World\" Geolocate to?",font_height=18))
    d.add(Box(m))

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()
```



