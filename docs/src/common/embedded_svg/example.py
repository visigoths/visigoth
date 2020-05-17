# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.common import EmbeddedSvg
from visigoth.common import Text

svg = """<?xml version="1.0" encoding="utf-8"?>
<svg height="100" version="1.1" width="100" xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <circle r="45" cx="50" cy="50" fill="orange" stroke="purple" stroke-width="10" />
</svg>
"""

d = Diagram()
d.add(Text("Embedded SVG!"))
d.add(EmbeddedSvg(svg,400,40))

html = d.draw(format="html")
f = open("example.html", "w")
f.write(html)
f.close()
