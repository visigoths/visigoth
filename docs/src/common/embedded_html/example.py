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

import argparse

from visigoth.diagram import Diagram
from visigoth.common import EmbeddedHtml

css = """
table td,th {
    border: 1px solid black;
}
table {
    border-collapse: collapse;
}
table caption {
    font-weight: bold;
}
"""

html1 = """
<button id="foo">Foo</button>
<script>
<![CDATA[
    document.getElementById("foo").onclick = function() {
        pubsubs_publish("%(id)s","click","click");
    };
]]>
</script>
"""

html2 = """
<script>
<![CDATA[
    pubsubs_subscribe("%(id)s","click",function(obj) { alert(obj); });
]]>
</script>
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    d = Diagram(fill="white")

    eh1 = EmbeddedHtml(html1,css,200,120)
    eh1.substituteHtml({"id":eh1.getId()})
    eh2 = EmbeddedHtml(html2,css,200,120)
    eh2.substituteHtml({"id":eh1.getId()})
    d.add(eh1)
    d.add(eh2)

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()
