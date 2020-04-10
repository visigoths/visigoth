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


import random
from math import radians,cos
import os

from visigoth.charts.som.hexgrid import HexGrid
from visigoth.utils.js import Js
from visigoth.charts.som.self_organising_map import SelfOrganisingMap
from visigoth.charts import ChartElement
from visigoth.utils.marker import MarkerManager
from visigoth.utils.colour import DiscretePalette

from visigoth.utils.data import Dataset


class SOM(ChartElement):

    """
    Create a Self Organising Map (SOM) chart with cells arranged in a hexagonal layout

    Arguments:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)
        width(int) : the width of the plot in pixels

    Keyword Arguments:
        colour (str or int): Identify the column to define the point colour (use palette default colour if not specified)
        label (str or int): Identify the column to define the label
        dimensions (str or int): Identify the column to define the vector of floats used to define the point dimensions
        gridwidth(int) : the number of columns in the SOM plot
        gridheight(int) : the number of rows in the SOM plot
        iters(int) : the number of training iterations to use when training the SOM
        palette(visigoth.utils.colour.DiscretePalette) : mapping from category to colour
        trainedSom(SelfOrganisingMap) : a pre-trained SOM model.  If specified, this SOM's grid width/height will be used
        marker_manager(object) : a MarkerManager instance to control marker appearance
        seed(int): random seed
        dimension(lambda): lambda to compute the dimension (from the values vector) value
        dimensionPalette(ContinuousPalette): a palette to map dimension values to colours
    """

    def __init__(self,data, width, label=0, colour=1, dimensions=2, gridwidth=10, gridheight=10, iters=100, palette=None, marker_manager=None, trainedSom=None, seed=None, dimension=None, dimensionPalette=None):
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

        if not palette:
            palette = DiscretePalette()
        self.setPalette(palette)

        self.iters = iters

        if not marker_manager:
            marker_manager = MarkerManager()
        self.setMarkerManager(marker_manager)

        self.fill = self.palette.getDefaultColour()
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
            self.som = SelfOrganisingMap(self.data, self.hexgrid, self.palette, self.gridwidth, self.gridheight, self.iters, seed=self.seed)
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

    def build(self):
        if not self.built:
            self.prepare()
            self.train()
            self.hexgrid.build()
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


