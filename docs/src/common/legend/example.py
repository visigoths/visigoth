# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.common import Legend
from visigoth.utils.colour import ContinuousPalette, DiscretePalette

discrete_palette = DiscretePalette()
discrete_palette.addCategory("A", "green").addCategory("B", "blue").addCategory("C", "red").addCategory("D", "orange").addCategory("E","purple")

continuous_palette = ContinuousPalette(withIntervals=False)

d = Diagram(fill="white")
d.add(Legend(discrete_palette,width=700, legend_columns=3))
d.add(Legend(continuous_palette,700))

html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

