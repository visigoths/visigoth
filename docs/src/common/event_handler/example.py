# -*- coding: utf-8 -*-

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

d = Diagram()

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

html = d.draw(format="html")
f = open("example.html", "w")
f.write(html)
f.close()
