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

import math
import random
from visigoth.svg import svgdoc, circle, polygon

def circumcircle(ax,ay,bx,by,cx,cy):
    # https://en.wikipedia.org/wiki/Circumscribed_circle
    D = 2 * ((ax*(by-cy)+bx*(cy-ay)+cx*(ay-by)))
    ux = 1/D * ((ax**2 + ay**2)*(by-cy)+(bx**2 + by**2)*(cy-ay)+(cx**2 + cy **2)*(ay - by))
    uy = 1/D * ((ax**2 + ay**2)*(cx-bx)+(bx**2 + by**2)*(ax-cx)+(cx**2 + cy **2)*(bx - ax))
    r = math.sqrt((ax-ux)**2+(ay-uy)**2)
    r2 = math.sqrt((bx-ux)**2+(by-uy)**2)
    r3 = math.sqrt((cx-ux)**2+(cy-uy)**2)
    return (ux,uy,r)

def in_circumcircle(p,tri):
    (t1,t2,t3) = tri
    (px,py) = p
    (ax,ay) = t1
    (bx,by) = t2
    (cx,cy) = t3
    (ux,uy,r) = circumcircle(ax,ay,bx,by,cx,cy)
    dist = math.sqrt((px-ux)**2 + (py-uy)**2)
    return dist < r

def edges(tri):
    ((ax,ay),(bx,by),(cx,cy)) = tri
    return [((ax,ay),(bx,by)),((ax,ay),(cx,cy)),((bx,by),(cx,cy))]

def has_edge(tri,edge):
    ((x1,y1),(x2,y2)) = edge
    redge = ((x1,y1),(x2,y2))
    tedges = edges(tri)
    return edge in tedges or redge in tedges

def common_vertex(tri1,tri2):
    p1 = list(tri1)
    p2 = list(tri2)

    for p in p1:
        if p in p2:
            return True
    return False

def bowyer_watson(points):
    # https://en.wikipedia.org/wiki/Bowyer%E2%80%93Watson_algorithm
    triangulation = []
    max_x = max([x for (x,y) in points])
    max_y = max([y for (x,y) in points])
    min_x = min([x for (x,y) in points])
    min_y = min([y for (x,y) in points])

    x_range = max_x - min_x
    y_range = max_y - min_y
    supertriangle = ((min_x-x_range*100,min_y-y_range*100),(max_x+x_range*100,0),(0,max_y+y_range*100))
    triangulation.append(supertriangle)
    for point in points:
        bad = []
        for triangle in triangulation:
            if in_circumcircle(point,triangle):
                bad.append(triangle)

        polygon = []
        for triangle in bad:
            for edge in edges(triangle):
                add = True
                for othertriangle in bad:
                    if othertriangle != triangle:
                        if has_edge(othertriangle,edge):
                            add = False
                if add:
                    polygon.append(edge)

        for triangle in bad:
            triangulation.remove(triangle)

        for edge in polygon:
            ((x1,y1),(x2,y2)) = edge
            newtriangle = ((x1,y1),(x2,y2),point)
            triangulation.append(newtriangle)

    return [triangle for triangle in triangulation if not common_vertex(triangle,supertriangle)]

if __name__ == '__main__':

    rng = random.Random()

    points = [(rng.random(),rng.random()) for x in range(10)]
    scale = 400
    doc = svgdoc(scale,scale)

    triangles = bowyer_watson(points)
    for triangle in triangles:
        p = polygon([(x*scale,y*scale) for (x,y) in list(triangle)],"white","green",2)
        doc.add(p)

    for point in points:
        c = circle(point[0]*scale,point[1]*scale,10,"red")
        doc.add(c)

    open("bw.svg","w+b").write(doc.render())
