# -*- coding: utf-8 -*-

from visigoth.diagram import Diagram
from visigoth.charts import Table

d = Diagram()

txt = """Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque 
laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto 
beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut 
odit aut fugit, sed quia consequuntur magni dolores eos qui ratione voluptatem sequi nesciunt. 
Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit, 
sed quia non numquam eius modi tempora incidunt ut labore et dolore magnam aliquam quaerat voluptatem. 
Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipit laboriosam, 
nisi ut aliquid ex ea commodi consequatur? Quis autem vel eum iure reprehenderit qui in ea 
voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas 
nulla pariatur?"""

lines = txt.replace("\n","").split(".")

columns = [0,1]
headings = ["column1","column2"]
formatters = [lambda x:"%0.2f"%x,None]

data = [[idx+1,lines[idx]] for idx in range(len(lines))]
t = Table(data,columns=columns,headings=headings,formatters=formatters,max_column_width=400)
t.setLeftJustified()
d.add(t)
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()
