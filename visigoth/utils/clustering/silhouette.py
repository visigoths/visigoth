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

class Silhouette(object):

    """
    Silhouette Cluster Evaluation

    Arguments:
        data(list) : list of (lon,lat) pairs to evaluate
        model : a cluster model implementing the score method

    """

    def __init__(self, data, model):
        self.data = data
        self.model = model

    def computeMeanDistance(self,point,otherpoints):
        totaldist = 0.0
        if len(otherpoints) == 0:
            return 0.0
        for otherpoint in otherpoints:
            totaldist += self.model.computeDistance(point,otherpoint)
        return totaldist/len(otherpoints)

    def compute(self):
        clusters = self.model.getClusterCount()
        assignments = {cluster:[] for cluster in range(clusters)}
        for point in self.data:
            cluster = self.model.score(point)
            assignments[cluster].append(point)

        s_tot = 0
        for point in self.data:
            cluster = self.model.score(point)
            sameclusterpoints = assignments[cluster][:]
            sameclusterpoints.remove(point)
            if not len(sameclusterpoints):
                continue
            sil_a = self.computeMeanDistance(point,sameclusterpoints)

            otherclusters = list(range(clusters))
            otherclusters.remove(cluster)
            sil_b = None
            for othercluster in otherclusters:
                otherclusterpoints = assignments[othercluster]
                b_cand = self.computeMeanDistance(point,otherclusterpoints)
                if b_cand > 0.0 and (sil_b == None or b_cand < sil_b):
                    sil_b = b_cand

            s_tot += (sil_b - sil_a)/max(sil_a,sil_b)
        return s_tot / len(self.data)