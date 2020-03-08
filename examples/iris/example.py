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
import random
import csv

from visigoth.diagram import Diagram
from visigoth.common import Text, Space, Legend
from visigoth.containers import Grid
from visigoth.charts import ScatterPlot
from visigoth.utils.colour import DiscretePalette

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    rng = random.Random()
    d = Diagram(fill="white")

    data = []
    reader = csv.reader(open("iris.csv"))
    keys = {}
    data = []
    for line in reader:
        if not keys:
            for idx in range(0,len(line)):
                keys[line[idx]] = idx
        else:
            data.append({k:line[keys[k]] for k in keys})

    p = DiscretePalette()
    g = Grid()
    p.addCategory("setosa","red").addCategory("virginica","blue").addCategory("versicolor","green")    
    
    fields = ["sepal_length","sepal_width","petal_length","petal_width"]

    def createPlot(x_field,y_field,data,palette):
        sdata = [(float(row[x_field]),float(row[y_field]),row["species"],row["species"],5) for row in data]
        sp = ScatterPlot(sdata,width=250,height=250,palette=palette)
        (ax,ay) = sp.getAxes()
        ax.setLabel(x_field)
        ay.setLabel(y_field)
        return sp

    l = Legend(p,width=800,legend_columns=3)

    for r in range(len(fields)):
        for c in range(len(fields)):
            x_field = fields[r]
            y_field = fields[c]
            if x_field == y_field:
                e = Text(x_field)
            else:
                e = createPlot(x_field,y_field,data,p)
                d.connect(l,"brushing",e,"brushing")
            g.add(r,c,e)

    d.add(g)
    d.add(l)
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

