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

import unittest
import random
import math

from visigoth import Diagram
from visigoth.utils.test_utils import TestUtils
from visigoth.containers.map import Map
from visigoth.containers.box import Box
from visigoth.map_layers.cluster import Cluster, AgglomerativeAlgorithm, KMeansAlgorithm

class TestCluster(unittest.TestCase):

    def test_basic(self):
        d = Diagram(fill="white")

        m1 = Map(512,boundaries=((0,0),(1,1)))
        rng = random.Random(1)

        data1 = [(rng.random(), rng.random()) for x in range(0, 100)]

        km = KMeansAlgorithm(cluster_count_min=3,cluster_count_max=8)
        
        m1.addLayer(Cluster(data1,algorithm=km))
        d.add(Box(m1))

        m2 = Map(512, boundaries=((0, 0), (1, 1)))

        angles2a = [math.pi * rng.random() for r in range(60)]
        data2a = [(0.4 + (0.35+rng.random()*0.1) * math.sin(a), 0.4 + 0.4 * math.cos(a)) for a in angles2a]
        angles2b = [math.pi + (math.pi * rng.random()) for r in range(60)]
        data2b = [(0.6 + (0.35+rng.random()*0.1) * math.sin(a), 0.6 + 0.4 * math.cos(a)) for a in angles2b]
        
        alg = AgglomerativeAlgorithm(max_distance=10000)
        m2.addLayer(Cluster(data2a+data2b,algorithm=alg,fill=("green","blue","orange","yellow"),radius=10,stroke="grey",stroke_width=2))

        d.add(Box(m2))
        svg = d.draw()
        TestUtils.output(svg,"test_cluster.svg")

if __name__ == '__main__':
    tc = TestCluster()
    tc.test_basic()