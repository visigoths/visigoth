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


import os.path
import sys
import argparse
import random

from visigoth.diagram import Diagram
from visigoth.charts.wordcloud import WordCloud
from visigoth.utils.colour import DiscretePalette
from visigoth.common.legend import Legend
from visigoth.utils.httpcache import HttpCache
from visigoth.containers.box import Box

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--outpath", help="path for output SVG", default="example.svg")
    args = parser.parse_args()

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

    data = sorted([(word,random.choice(["A","B","C","D"]),freqs[word]) for word in freqs],key=lambda x:x[2],reverse=True)[:100]
    d = Diagram()
    
    wc = WordCloud(data, 600, 600, palette, text_attributes={"font-weight":"bold"}, flip_fraction=0.1)
    d.add(Box(wc,fill="lightgrey"))
    l = Legend(palette,legend_columns=4)
    d.add(l)

    d.connect(l,"brushing",wc,"brushing")
    d.connect(wc,"brushing",l,"brushing")
    svg = d.draw()

    f = open(args.outpath, "wb")
    f.write(svg)
    f.close()

