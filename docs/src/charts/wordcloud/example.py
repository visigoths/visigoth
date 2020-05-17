# -*- coding: utf-8 -*-

import os.path
import sys
import random

from visigoth import Diagram
from visigoth.charts import WordCloud
from visigoth.utils.colour import DiscretePalette
from visigoth.common import Legend
from visigoth.utils.httpcache import HttpCache
from visigoth.containers import Box

palette = DiscretePalette()
palette.addCategory("A","green").addCategory("B","blue").addCategory("C","red").addCategory("D","purple")

folder = os.path.split(sys.argv[0])[0]
path = HttpCache.fetch("https://gutenberg.ca/ebooks/huxleya-bravenewworld/huxleya-bravenewworld-00-t.txt",suffix=".txt",returnPath=True)
brave_new_world = open(path,"r",encoding="cp852").read()

words = brave_new_world.replace(","," ").split(" ")
freqs = {}
isValid = lambda x: len(x)>5
for word in words:
    word = word.lower()
    if isValid(word):
        if word not in freqs:
            freqs[word] = 1
        else:
            freqs[word] += 1

# plot the 100 most frequently occurring words
data = sorted([(word,random.choice(["A","B","C","D"]),freqs[word]) for word in freqs],
              key=lambda x:x[2],reverse=True)[:100]
d = Diagram()
wc = WordCloud(data, palette=palette, text_attributes={"font-weight":"bold"}, flip_fraction=0.1)
d.add(Box(wc,fill="lightgrey"))
l = Legend(palette,legend_columns=4)
d.add(l)

d.connect(l,"colour",wc,"colour")
d.connect(wc,"colour",l,"colour")
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

