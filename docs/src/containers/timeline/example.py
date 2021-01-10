# -*- coding: utf-8 -*-

import datetime

from visigoth import Diagram
from visigoth.containers import TimeLine, Box
from visigoth.charts import Bar
from visigoth.common import Legend, Text
from visigoth.utils.colour import DiscreteColourManager

timeline1 = TimeLine(orientation="vertical")
timeline2 = TimeLine(orientation="horizontal")

colour_manager = DiscreteColourManager()
colour_manager.addColour("A","#E7FFAC").addColour("B","#FFC9DE")
colour_manager.addColour("C","#B28DFF").addColour("D","#ACE7FF")

data1 = [("A",10),("B",5),("C",-4),("D",3)]
data2 = [("A",8),("B",2),("C",-1),("D",6)]
data3 = [("A",3),("B",5),("C",2),("D",-3)]

d = Diagram()

bar1 = Bar(data1, colour=0, width=400, height=400, colour_manager=colour_manager)
bar2 = Bar(data2, colour=0, width=200, height=200, colour_manager=colour_manager)
bar3 = Bar(data3, colour=0, width=200, height=200, colour_manager=colour_manager)

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
legend = Legend(colour_manager=colour_manager,legend_columns=4,width=768)
d.add(legend)
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()


