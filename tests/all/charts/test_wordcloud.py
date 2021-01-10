# -*- coding: utf-8 -*-

#    visigoth: A lightweight Python3 library for rendering data visualizations in SVG
#    Copyright (C) 2020  Niall McCarroll
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy of this software
#   and associated documentation files (the "Software"), to deal in the Software without 
#   restriction, including without limitation the rights to use, copy, modify, merge, publish,
#   distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all copies or 
#   substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
#   BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
#   NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#   DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os.path
import sys
import argparse

import unittest

from visigoth.diagram import Diagram
from visigoth.charts.wordcloud import WordCloud
from visigoth.utils.colour import DiscreteColourManager
from visigoth.common.space import Space
from visigoth.common.legend import Legend
from visigoth.common.text import Text
from visigoth.containers.box import Box

from visigoth.utils.test_utils import TestUtils

class TestWordCloud(unittest.TestCase):

    def test_basic(self):

        colour_manager = DiscreteColourManager()
        colour_manager.addColour("A","green").addColour("B","blue").addColour("C","red").addColour("D","purple")

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

        d.add(Box(WordCloud(data, width=600, height=600, colour_manager=colour_manager, text_attributes={"font-weight":"bold"}, flip_fraction=0.1),fill="lightgrey"))

        d.add(Box(WordCloud(data, width=600, height=600, colour_manager=colour_manager, text_attributes={"font-weight":"bold"}, flip_fraction=0.0)))

        TestUtils.draw_output(d,"test_wordcloud")

if __name__ == "__main__":
    unittest.main()