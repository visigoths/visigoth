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


### Credits/Acknowledgements/Citations

This project uses matrix inversion code from Andrew Ippoliti's Blog.  See http://blog.acipo.com/matrix-inversion-in-javascript/

This project re-uses sequences of RGB colour codes from the following color maps:

* Continuous Color Maps (Viridis, Magma, Plasma and Inferno):

```
License regarding the Viridis, Magma, Plasma and Inferno colormaps:
New matplotlib colormaps by Nathaniel J. Smith, Stefan van der Walt,
and (in the case of viridis) Eric Firing.

The Viridis, Magma, Plasma, and Inferno colormaps are released under the
CC0 license / public domain dedication. We would appreciate credit if you
use or redistribute these colormaps, but do not impose any legal
restrictions.

To the extent possible under law, the persons who associated CC0 with
mpl-colormaps have waived all copyright and related or neighboring rights
to mpl-colormaps.

You should have received a copy of the CC0 legalcode along with this
work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.
```

* Discrete Colour Maps (deep, deep6, muted=, muted6, pastel, pastel6, bright, bright6, dark, dark6, colorblind, colorblind6):

```
Copyright (c) 2012-2020, Michael L. Waskom
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the project nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```