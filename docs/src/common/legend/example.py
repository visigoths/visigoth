# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.common import Legend
from visigoth.utils.colour import ContinuousColourManager, DiscreteColourManager

discrete_colour_manager = DiscreteColourManager()
discrete_colour_manager.addColour("A", "green").addColour("B", "blue").addColour("C", "red").addColour("D", "orange").addColour("E","purple")

continuous_colour_manager = ContinuousColourManager(withIntervals=False)
continuous_colour_manager.allocateColour(0)
continuous_colour_manager.allocateColour(10)

d = Diagram(fill="white")
d.add(Legend(discrete_colour_manager,width=700, legend_columns=3))
d.add(Legend(continuous_colour_manager,700))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

