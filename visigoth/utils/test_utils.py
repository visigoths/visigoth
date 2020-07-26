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

import os

class TestUtils(object):

    def __init__(self):
        pass

    @staticmethod
    def output(content,filename):

        with open(filename, "w") as f:
            f.write(content)

    @staticmethod
    def draw_output(diagram, filename):
        suffix = os.path.splitext(filename)[1]
        tasks = []
        if suffix == ".svg":
            tasks = [("svg",filename)]
        elif suffix == ".html":
            tasks = [("html",filename)]
        elif suffix == "":
            tasks = [("html",filename+".html"),("svg",filename+".svg")]
        if tasks == []:
            raise Exception(suffix)

        for (format,path) in tasks:
            content = diagram.draw(format=format)
            with open(path,"w") as f:
                f.write(content)
