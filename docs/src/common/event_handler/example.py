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
from visigoth.common import Button
from visigoth.common import EventHandler

jscode1 = """
function(channel,obj,config,sendfn)
{
    alert("Code 1: Got event channel="+channel+",value="+obj);
}
"""

jscode2 = """
function(channel,obj,config,sendfn)
{
    alert("Code 2: Got event channel="+channel+",value="+obj);
}
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    d = Diagram(fill="white")

    b1 = Button("Click Me!")
    b2 = Button("Or Click Me!")
    
    ev1 = EventHandler(jscode1,{})
    ev2 = EventHandler(jscode2,{})

    d.add(b1)
    d.add(b2)
    d.add(ev1)
    d.add(ev2)

    d.connect(b1,"click",ev1,"click")
    d.connect(b2,"click",ev2,"click")

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()
