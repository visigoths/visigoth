# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.charts import Transition
from visigoth.utils.colour import DiscreteColourManager
from visigoth.common import Legend, Space, Text

colour_manager = DiscreteColourManager()
colour_manager.addColour("Status A", "green").addColour("Status B", "blue").addColour("Status C", "red")

data = [
    ["M1", "","Status B","Status B","Status B"],
    ["M2", "Status A","","Status A","Status A"],
    ["M3", "Status B","Status C","Status B","Status C"],
    ["M4", "Status B", "Status A", "Status A", "Status C"],
    ["M5", "Status A","Status C","","Status C"],
    ["M6", "Status A","Status B","Status C","Status A"],
    ["M7", "Status B","Status C","Status C","Status C"],
    ["M8", "Status A","Status B","Status A","Status B"]
]

d = Diagram(fill="white")

d.add(Text("Status Changes Over 2 Hour Period",font_height=32,text_attributes={"stroke":"purple"}))
t = Transition(data,label=0,states=[1,2,3,4], width=1024, colour_manager=colour_manager,
               transition_labels=["10:00", "10:30","11:00","11:30"],y_axis_label="Count")
d.add(t)
d.add(Space(20,20))
l = Legend(colour_manager,1024, legend_columns=3)
d.add(l)

d.connect(t,"colour",l,"colour")
d.connect(l,"colour",t,"colour")

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

