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