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

class AgglomerativeAlgorithm(object):

    """
    Agglomerative algorithm

    Keyword Arguments:
        max_distance (int): do not cluster points that are further apart than this distance (metres)    
    """
    def __init__(self,max_distance=1000):
        self.max_distance = max_distance

    def train(self,data,projection):
        projected_data = map(lambda x:projection.fromLonLat(x),data)
        clusters = {}
        distances = {}
        cluster_id_counter = 0
        for (e,n) in projected_data:
            clusters[cluster_id_counter] = [(e,n)]
            cluster_id_counter += 1
        
        for cid1 in clusters:
            for cid2 in clusters:
                if cid1 < cid2:    
                    p1 = clusters[cid1][0]
                    p2 = clusters[cid2][0]
                    d = AgglomerativeAlgorithm.euclidean(p1,p2)
                    if d < self.max_distance:
                        distances[(cid1,cid2)] = d

        while len(distances)>0:
            min_dist = None
            min_pair = None
            for pair in distances:
                dist = distances[pair]
                if min_dist == None or dist < min_dist:
                    min_dist = dist
                    min_pair = pair
            (cid1,cid2) = min_pair
            items1 = clusters[cid1]
            items2 = clusters[cid2]
            combined_items = items1+items2
            combined_cid = cluster_id_counter
            cluster_id_counter += 1
            clusters[combined_cid] = combined_items
            
            del clusters[cid1]
            del clusters[cid2]
            new_distances = {}
            remove_list = [(cid1,cid2)]
            for (cid3,cid4) in distances:
                if (cid3,cid4) != (cid1,cid2):
                    if cid1 == cid3:
                        self.recompute_distance(combined_cid,cid1,cid4,distances,new_distances)
                        remove_list.append((cid3,cid4))
                    if cid2 == cid3:
                        self.recompute_distance(combined_cid,cid2,cid4,distances,new_distances)
                        remove_list.append((cid3,cid4))
                    if cid1 == cid4:
                        self.recompute_distance(combined_cid,cid1,cid3,distances,new_distances)
                        remove_list.append((cid3,cid4))
                    if cid2 == cid4:
                        self.recompute_distance(combined_cid,cid2,cid3,distances,new_distances)
                        remove_list.append((cid3,cid4))    
                
            for item in remove_list:
                del distances[item]
            for key in new_distances:
                distances[key] = new_distances[key]
                    
        # renumber clusters
        cluster_num = 0
        final_clusters = {}
        for cluster in clusters:
            final_clusters[cluster_num] = clusters[cluster]   
            cluster_num += 1     
        return AgglomerativeModel(projection,final_clusters)

    @staticmethod
    def euclidean(p1,p2):
        (x1,y1) = p1
        (x2,y2) = p2
        return math.sqrt((x1-x2)**2+(y1-y2)**2)        

    def recompute_distance(self,combined_cid,from_cid,to_cid,distances,new_distances):
        old_dist = distances[self.order_tuple((from_cid,to_cid))]
        if (to_cid,combined_cid) not in new_distances:
            new_distances[(to_cid,combined_cid)] = old_dist
        else:
            if new_distances[(to_cid,combined_cid)] > old_dist:
                new_distances[(to_cid,combined_cid)] = old_dist 

    def order_tuple(self,t):
        (v1,v2) = t
        if v1 > v2:
            return (v2,v1)
        else:
            return t

class AgglomerativeModel(object):

    def __init__(self,projection,clusters):
        self.projection = projection
        self.clusters = clusters

    def getClusterCount(self):
        return len(self.clusters)

    def score(self,point):
        ppoint = self.projection.fromLonLat(point)
        min_dist = None
        closest_cluster = None
        for cluster in self.clusters:
            cluster_points = self.clusters[cluster]
            for cluster_point in cluster_points:
                dist = AgglomerativeAlgorithm.euclidean(ppoint,cluster_point)
                if min_dist == None or dist < min_dist:
                    min_dist = dist
                    closest_cluster = cluster
        return closest_cluster
