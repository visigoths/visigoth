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
import sys
import math

from visigoth.utils.term.progress import Progress
from visigoth.utils.clustering.silhouette import Silhouette

class KMeansAlgorithm(object):

    def __init__(self,nr_attempts=3,cluster_count_min=2,cluster_count_max=10,iterations=200):
        self.nr_attempts = nr_attempts
        self.cmin = cluster_count_min
        self.cmax = cluster_count_max
        self.iterations = iterations
        
    def train(self,data,projection):
        sil_max = None
        best_model = None
        total_runs = ((self.cmax+1)-self.cmin)*self.nr_attempts
        progress_frac = 0.0
        p = Progress("KMeans Cluster")
        p.report("Starting",progress_frac)
        for count in range(self.cmin,self.cmax+1):
            for attempt in range(0,self.nr_attempts):
                progress_frac += 1/total_runs
                model = KMeans(data,count,self.iterations)
                
                model.setProjection(projection)
                model.train()

                s = Silhouette(data,model)
                sil = s.compute()
                
                if sil_max == None or sil > sil_max:
                    sil_max = sil
                    best_model = model
                p.report("trying %d clusters"%(count),progress_frac)
        p.complete("Complete")
        return best_model

class KMeans(object):

    """
    KMeans algorithm

    Arguments:
        data(list) : list of (lon,lat) pairs to cluster

    Keyword Arguments:
        centers (int): the number of centers to discover
        iterations (int): the number of algorith iterations to run
        seed (int): a random seed to set

    """

    def __init__(self, data, centers=5, iterations=1000,seed=None):
        self.input_data = data
        self.data = []
        self.centers = centers
        self.iterations = iterations
        self.seed = seed


    def getClusterCount(self):
        return self.centers

    def getCentroids(self):
        return self.centroids

    def setProjection(self,projection):
        self.projection = projection

    def score(self,point):
        return self.findNearestCentroid(self.projection.fromLonLat(point))

    def computeDistance(self,point1,point2):
        return self.euclidean(self.projection.fromLonLat(point1),self.projection.fromLonLat(point2))

    def euclidean(self,p1,p2):
        (x1,y1) = p1
        (x2,y2) = p2
        return math.sqrt((x1-x2)**2+(y1-y2)**2)

    def findNearestCentroid(self,point):
        mind = None
        minc = None
        for centroid_idx in range(0,len(self.centroids)):
            centroid = self.centroids[centroid_idx]
            d = self.euclidean(point,centroid)
            if mind == None or d < mind:
                 mind = d
                 minc = centroid_idx
        return minc

    def iterate(self):
        clusters = {c:[] for c in range(self.centers)}
        for datapoint in self.data:
            clusters[self.findNearestCentroid(datapoint)].append(datapoint)

        # update centroids
        for cluster in clusters:
            assignments = clusters[cluster]
            if assignments:
                count = len(assignments)
                xmean = sum([x for (x,y) in assignments])/count
                ymean = sum([y for (x,y) in assignments])/count
                self.centroids[cluster] = (xmean,ymean)

    def train(self):

        self.data = [self.projection.fromLonLat(p) for p in self.input_data]

        self.minx = min([x for (x,y) in self.data])
        self.miny = min([y for (x,y) in self.data])
        self.maxx = max([x for (x,y) in self.data])
        self.maxy = max([y for (x,y) in self.data])
        self.rng = random.Random()

        self.centroids = [(self.minx+self.rng.random()*(self.maxx-self.minx),
            self.miny+self.rng.random()*(self.maxy-self.miny)) for c in range(self.centers)]

        for i in range(self.iterations):
            self.iterate()