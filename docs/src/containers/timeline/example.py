# -*- coding: utf-8 -*-
# Copyright 2017-2018 Niall McCarroll
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import sys
import datetime

from visigoth import Diagram
from visigoth.containers import TimeLine, Box
from visigoth.charts import Bar
from visigoth.common import Legend, Text
from visigoth.utils.colour import DiscretePalette

if __name__ == "__main__":

    folder = os.path.split(__file__)[0]

    timeline1 = TimeLine(orientation="vertical")
    timeline2 = TimeLine(orientation="horizontal")

    palette = DiscretePalette()
    palette.addCategory("A","#E7FFAC").addCategory("B","#FFC9DE")
    palette.addCategory("C","#B28DFF").addCategory("D","#ACE7FF")

    data1 = [("A",10),("B",5),("C",-4),("D",3)]
    data2 = [("A",8),("B",2),("C",-1),("D",6)]
    data3 = [("A",3),("B",5),("C",2),("D",-3)]

    d = Diagram(fill="white")

    bar1 = Bar(data1, width=400, height=400, palette=palette)
    bar2 = Bar(data2, width=200, height=200, palette=palette)
    bar3 = Bar(data3, width=200, height=200, palette=palette)

    timeline1.add(datetime.datetime(2016,1,1,0,0,0),None,"2016")
    timeline1.add(datetime.datetime(2017,1,1,0,0,0),Box(bar1),"2017",offset=100)
    timeline1.add(None,Box(Text("Hello World")),None,offset=100)
    timeline1.add(datetime.datetime(2018,1,1,0,0,0),Box(bar2),"2018",offset=150)
    timeline1.add(datetime.datetime(2019,1,1,0,0,0),Box(bar2),"2019",offset=120)
    timeline1.add(datetime.datetime(2020,1,1,0,0,0),None,"2020")

    timeline2.add(datetime.datetime(2016,1,1,0,0,0),None,"2016")
    timeline2.add(datetime.datetime(2017,1,1,0,0,0),Box(bar1),"2017",offset=50)
    timeline2.add(datetime.datetime(2018,1,1,0,0,0),Box(bar2),"2018",offset=120)
    timeline2.add(datetime.datetime(2019,1,1,0,0,0),Box(bar2),"2019",offset=90)
    timeline2.add(datetime.datetime(2020,1,1,0,0,0),None,"2020")

    d.add(timeline1).add(timeline2)
    legend = Legend(palette=palette,legend_columns=4,width=768)
    d.add(legend)
    svg = d.draw()

    outputpath=os.path.join(folder,"example.svg")
    f = open(outputpath, "wb")
    f.write(svg)
    f.close()

