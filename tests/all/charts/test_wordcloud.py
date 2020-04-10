# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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

import unittest

from visigoth.diagram import Diagram
from visigoth.charts.wordcloud import WordCloud
from visigoth.utils.colour import DiscretePalette
from visigoth.common.space import Space
from visigoth.common.legend import Legend
from visigoth.common.text import Text
from visigoth.containers.box import Box

from visigoth.utils.test_utils import TestUtils

class TestWordCloud(unittest.TestCase):

    def test_basic(self):

        palette = DiscretePalette()
        palette.addCategory("A","green").addCategory("B","blue").addCategory("C","red").addCategory("D","purple")

        d = Diagram()
    
        data = [
            ("something","A",100),
            ("midnight","A",90),
            ("hover","B",40),
            ("finally","C",50),
            ("familiar","C",40),
            ("tiger","D",60),
            ("super","D",70),
            ("basement","D",40),
            ("stereotype","B",20),
            ("motorcycle","B",20),
            ("snail","C",30),
            ("badass","D",130)]

        d.add(Box(WordCloud(data, width=600, height=600, palette=palette, text_attributes={"font-weight":"bold"}, flip_fraction=0.1),fill="lightgrey"))

        d.add(Box(WordCloud(data, width=600, height=600, palette=palette, text_attributes={"font-weight":"bold"}, flip_fraction=0.0)))

        svg = d.draw()
        TestUtils.output(svg,"test_wordcloud.svg")

if __name__ == "__main__":
    unittest.main()