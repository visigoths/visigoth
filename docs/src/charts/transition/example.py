# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

from visigoth import Diagram
from visigoth.charts import Transition
from visigoth.utils.colour import DiscretePalette
from visigoth.common import Legend, Space, Text
from visigoth.containers import Box


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    palette = DiscretePalette()
    palette.addCategory("Status A", "green").addCategory("Status B", "blue").addCategory("Status C", "red")

    machine_states = {
        "M1": ("","Status B","Status B","Status B"),
        "M2": ("Status A","","Status A","Status A"),
        "M3": ("Status B","Status C","Status B","Status C"),
        "M4": ("Status B", "Status A", "Status A", "Status C"),
        "M5": ("Status A","Status C","","Status C"),
        "M6": ("Status A","Status B","Status C","Status A"),
        "M7": ("Status B","Status C","Status C","Status C"),
        "M8": ("Status A","Status B","Status A","Status B")
    }

    d = Diagram(fill="white")

    d.add(Text("Status Changes Over 2 Hour Period",font_height=32,text_attributes={"stroke":"purple"}))
    t = Transition(1024,512,machine_states,palette,["10:00", "10:30","11:00","11:30"],y_axis_label="Count")
    d.add(t)
    d.add(Space(20,20))
    l = Legend(palette,1024, legend_columns=3)
    d.add(l)

    d.connect(t,"brushing",l,"brushing")
    d.connect(l,"brushing",t,"brushing")

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

