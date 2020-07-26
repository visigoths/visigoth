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
from visigoth.utils.term.progress import Progress

class SelfOrganisingMap(object):

    """
    Train Self Organising Map (SOM) with cells arranged in a hexagonal layout

    Arguments:
        data(list) : data in the form of a list of (label,category,float_list) pairs where float_list is a list of floats
        gridwidth(int) : number of cells across the grid
        gridheight(int) : number of cells down the grid
        iters(int) : the number of training iterations to use when training the SOM

    Keyword Arguments:
        seed(int) : random seed - set to produce repeatable results
    """

    def __init__(self,data, hexgrid, palette, gridwidth, gridheight, iters, seed=None):
        self.hexgrid = hexgrid
        self.palette = palette
        self.gridheight = gridheight
        self.gridwidth = gridwidth
        self.iters = iters

        self.learnRate_initial = 0.5
        self.learnRate_final = 0.05

        self.seed = seed
        if self.seed != None:
            random.seed(self.seed)

        self.rng = random.Random()
        self.weights = []
        self.oactivations = []

        self.neighbour_limit = 0
        self.learnRate = 0
        self.nrWeights = 0

        self.initial_neighbourhood = 4
        self.instances = data
        self.scores = {}

        self.nrInputs = len(self.instances[0][2])
        self.nrOutputs = self.gridwidth * self.gridheight
        self.nrWeights = self.nrOutputs * self.nrInputs

        for w in range(0,self.nrWeights):
            self.weights.append((self.rng.random()/5.0)+0.4)

        for oa in range(0,self.nrOutputs):
            self.oactivations.append(0.0)

    def getGridWidth(self):
        return self.gridwidth

    def getGridHeight(self):
        return self.gridheight

    def getWeights(self,outputIndex):
        return self.weights[(self.nrInputs * outputIndex):(self.nrInputs * (outputIndex + 1))]

    def train(self):
        p = Progress("SOM")
        progress_frac = 0.0
        p.report("Starting",progress_frac)
        iteration = 0
        while iteration < self.iters:
            self.learnRate = (1.0 - float(iteration) / float(self.iters)) * (self.learnRate_initial - self.learnRate_final) + self.learnRate_final
            self.neighbour_limit = self.initial_neighbourhood - int(
                (float(iteration) / float((self.iters + 1))) * self.initial_neighbourhood)
            # print("iter=%d (of %d) / learning-rate=%f / neighbourhood=%d"%(iteration,self.iters,self.learnRate,self.neighbour_limit))
            for (label,category,instance) in self.instances:
                winner = self.computeActivations(instance)
                self.updateNetwork(winner,instance)

            iteration += 1
            progress_frac = iteration/self.iters
            p.report("Training neighbourhood=%d"%(self.neighbour_limit),progress_frac)

        p.complete("SOM Training Complete")

        self.scores = {(xc, yc): [] for xc in range(0, self.gridwidth) for yc in range(0, self.gridheight)}

        for (label, category, instance) in self.instances:
            winner_coords = self.coords(self.computeActivations(instance))
            colour = ""
            if category and self.palette:
                colour = self.palette.getColour(category)
            self.scores[winner_coords].append((label,colour,category))

    def getScores(self):
        return self.scores

    def computeActivations(self,iactivations):
        mindistance = None
        winner = -1
        # inarr = numpy.array(iactivations)
        for idx in range(0,self.nrOutputs):
            self.oactivations[idx] = self.distance(iactivations,self.weights[(self.nrInputs*idx):(self.nrInputs*(idx+1))])
            # self.oactivations[idx] = numpy.linalg.norm(inarr-numpy.array(self.getWeights(idx)))
            if winner == -1:
                mindistance = self.oactivations[idx]
                winner = idx
            else:
                if mindistance > self.oactivations[idx]:
                    mindistance = self.oactivations[idx]
                    winner = idx
        return winner

    def updateNetwork(self,winner,iactivations):
        for idx in range(0,self.nrOutputs):
            if self.isNeighbour(idx,winner):
                self.adjustWeights(idx,iactivations)

    def isNeighbour(self,output,winner):
        (ox,oy) = self.coords(output)
        (wx,wy) = self.coords(winner)
        neighbour_distance = self.hexgrid.getDistance(ox,oy,wx,wy)
        return neighbour_distance and neighbour_distance <= self.neighbour_limit

    def coords(self,output):
        return (output % self.gridwidth, output // self.gridwidth)

    def getOutput(self,x,y):
        return x + (y*self.gridwidth)

    def getDimensionValue(self,dimensionFn,x,y):
        output = self.getOutput(x,y)
        pos = (output*self.nrInputs)
        cellweights = self.weights[pos:pos+self.nrInputs]
        return dimensionFn(cellweights)

    def distance(self,array1,array2):
        total = 0.0
        for idx in range(0,len(array1)):
            dist = array1[idx]-array2[idx]
            total += (dist*dist)
        return total

    def adjustWeights(self,output,iactivations):
        for idx in range(0,self.nrInputs):
            wpos = (output*self.nrInputs)+idx
            w = self.weights[wpos]
            i = iactivations[idx]
            w = w + (self.learnRate * (i - w))
            self.weights[wpos] = w



