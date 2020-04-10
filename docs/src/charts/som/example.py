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

import csv
import argparse
from visigoth import Diagram
from visigoth.charts import SOM
from visigoth.common import Text, Legend
from visigoth.utils.colour import ContinuousPalette

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

    cpalette0 = ContinuousPalette(withIntervals=False)
    cpalette0.addColour("#000000",0.0).addColour("red",1.0)

    cpalette1 = ContinuousPalette(withIntervals=False)
    cpalette1.addColour("#000000",0.0).addColour("red",1.0)

    cpalette2 = ContinuousPalette(withIntervals=False)
    cpalette2.addColour("#000000",0.0).addColour("blue",1.0)

    cpalette3 = ContinuousPalette(withIntervals=False)
    cpalette3.addColour("#000000",0.0).addColour("white",1.0)

    min_temp_data = []
    max_temp_data = []
    precipitation_data = []
    snowfall_data = []
    reader = csv.reader(open("climate_by_city.csv"))
    headers_read = False
    for line in reader:
        if not headers_read:
            headers_read = True
        else:
            label = line[0]
            cat = ""
            values = list(map(lambda s:float(s),line[1:]))
            min_temp_data.append((label,cat,values[0:12]))
            max_temp_data.append((label,cat,values[12:24]))
            precipitation_data.append((label,cat,values[24:36]))
            snowfall_data.append((label,cat,values[36:48]))

    def mean(vec):
        return sum(vec)/len(vec)

    d = Diagram(fill="white")

    som0 = SOM(min_temp_data,512,dimension=lambda l: mean(l),dimensionPalette=cpalette0)
    som1 = SOM(max_temp_data,512,dimension=lambda l: mean(l),dimensionPalette=cpalette1)
    som2 = SOM(precipitation_data,512,dimension=lambda l: mean(l),dimensionPalette=cpalette2)
    som2.getPalette().setDefaultColour("white")

    d.add(Text("Cities clustered by monthly minimum temperature(s)"))
    d.add(som0)
    d.add(Text("Mean minimum daily temperature (Celsius)",font_height=12))
    d.add(Legend(cpalette0,width=500))

    d.add(Text("Cities clustered by monthly maximum temperature(s)"))
    d.add(som1)
    d.add(Text("Mean maximum daily temperature (Celsius)",font_height=12))
    d.add(Legend(cpalette1,width=500))

    d.add(Text("Cities clustered by precipitation"))
    d.add(som2)
    d.add(Text("Mean daily precipitation (mm)",font_height=12))
    d.add(Legend(cpalette2,width=500))

    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

