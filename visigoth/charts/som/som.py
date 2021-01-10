# -*- coding: utf-8 -*-

#    Visigoth: A lightweight Python3 library for rendering data visualizations in SVG
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


import random
from math import radians,cos
import os

from visigoth.charts.som.hexgrid import HexGrid
from visigoth.utils.js import Js
from visigoth.charts.som.self_organising_map import SelfOrganisingMap
from visigoth.charts import ChartElement
from visigoth.utils.marker import MarkerManager
from visigoth.utils.colour import DiscreteColourManager

from visigoth.utils.data import Dataset


class SOM(ChartElement):

    """
    Create a Self Organising Map (SOM) chart with cells arranged in a hexagonal layout

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)
        width(int) : the width of the plot in pixels

    Keyword Arguments:
        colour (str or int): Identify the column to define the point colour (use colour_manager default colour if not specified)
        label (str or int): Identify the column to define the label
        dimensions (str or int): Identify the column to define the vector of floats used to define the point dimensions
        gridwidth(int) : the number of columns in the SOM plot
        gridheight(int) : the number of rows in the SOM plot
        iters(int) : the number of training iterations to use when training the SOM
        colour_manager(visigoth.utils.colour.DiscreteColourManager) : mapping from category to colour
        trainedSom(SelfOrganisingMap) : a pre-trained SOM model.  If specified, this SOM's grid width/height will be used
        marker_manager(object) : a MarkerManager instance to control marker appearance
        seed(int): random seed
        dimension(lambda): lambda to compute the dimension (from the values vector) value
        dimensionPalette(ContinuousColourManager): a colour_manager to map dimension values to colours
    """

    def __init__(self,data, width, label=0, colour=1, dimensions=2, gridwidth=10, gridheight=10, iters=100, colour_manager=None, marker_manager=None, trainedSom=None, seed=None, dimension=None, dimensionPalette=None):
        super(SOM, self).__init__()
        self.width = width
        dataset = Dataset(data)
        self.data = dataset.query([label,colour,dimensions])
        if trainedSom:
            self.gridwidth = trainedSom.getGridWidth()
            self.gridheight = trainedSom.getGridHeight()
        else:
            self.gridheight = gridheight
            self.gridwidth = gridwidth

        if not colour_manager:
            colour_manager = DiscreteColourManager()
        self.setPalette(colour_manager)

        self.iters = iters

        if not marker_manager:
            marker_manager = MarkerManager()
        self.setMarkerManager(marker_manager)

        self.fill = self.colour_manager.getDefaultColour()
        self.stroke = self.marker_manager.getStroke()
        self.stroke_width = self.marker_manager.getStrokeWidth()

        self.seed = seed
        if self.seed != None:
            random.seed(self.seed)

        self.built = False

        self.initial_neighbourhood = 4

        self.scores = {}

        self.dimensionFn = dimension
        self.dimensionPalette = dimensionPalette
        self.instanceRadius = self.marker_manager.getDefaultRadius()

        heightWidthRatio = cos(radians(30))*self.gridheight/self.gridwidth

        self.height = self.width * heightWidthRatio
        self.som = trainedSom

    def prepare(self):
        self.hexgrid = HexGrid(self.width, self.gridwidth, self.gridheight, self.initial_neighbourhood,self.fill,self.stroke,self.stroke_width, self.dimensionFn, self.dimensionPalette, self.instanceRadius)
        if self.som:
            self.som_trained = True
        else:
            self.som_trained = False
            self.som = SelfOrganisingMap(self.data, self.hexgrid, self.colour_manager, self.gridwidth, self.gridheight, self.iters, seed=self.seed)
        self.hexgrid.setModel(self.som)
        self.plot = None

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getWeights(self,outputIndex):
        return self.weights[(self.nrInputs * outputIndex):(self.nrInputs * (outputIndex + 1))]

    def train(self):
        if not self.som_trained:
            self.som.train()
            self.som_trained = True
        return self.som

    def build(self,fmt):
        if not self.built:
            self.prepare()
            self.train()
            self.hexgrid.build(fmt)
            self.scores = self.som.getScores()
            self.built = True

    def drawChart(self,doc,cx,cy,chart_width,chart_height):

        oy = cy - self.height/2
        ox = cx - self.width/2

        categories = {}

        self.hexgrid.renderGrid(doc,ox,oy,self.scores,categories)

        with open(os.path.join(os.path.split(__file__)[0],"som.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = { "element_class_map": self.hexgrid.getElementClassMap(), "categories": categories }
        Js.registerJs(doc,self,jscode,"som",cx,cy,config)

        return config


