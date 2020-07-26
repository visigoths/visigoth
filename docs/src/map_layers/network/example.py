# -*- coding: utf-8 -*-

from visigoth import Diagram
from visigoth.containers import Box, Map
from visigoth.common import Legend
from visigoth.map_layers import Network, WMS
from visigoth.map_layers.network import DDPageRank
from visigoth.utils.colour import ContinuousPalette
from visigoth.utils.marker import MarkerManager

d = Diagram()

m1 = Map(512,width_to_height=1)

nodes = [('0', -0.463, 40.588), ('1', -0.769, 40.170),
 ('2', -0.535, 40.538), ('3', -0.613, 40.026),
 ('4', -0.868, 40.759), ('5', -0.408, 40.343),
 ('6', -0.402, 40.755), ('7', -0.197, 40.580),
 ('8', -0.257, 40.688), ('9', -0.381, 40.518)]

edges = [
    ('2', '0'), ('1', '3'), ('7', '8'), ('4', '2'), ('7', '9'), ('8', '7'), ('6', '8'), ('4', '0'), ('0', '2'),
 ('8', '6'), ('3', '1'), ('0', '9'), ('5', '9'), ('1', '5'), ('9', '0'), ('5', '2'), ('1', '2'), ('8', '9'),
 ('4', '6'), ('6', '0')]

palette = ContinuousPalette()
mm = MarkerManager().setDefaultRadius(10)

nw = Network(node_data=nodes,edge_data=edges,marker_manager=mm,palette=palette,ranking_algorithm=DDPageRank())
m1.add(WMS("osm").setOpacity(0.5))
m1.add(nw)
d.add(Box(m1))
d.add(Legend(palette,512))
html = d.draw(format="html")

f = open("example.html", "w")
f.write(html)
f.close()

