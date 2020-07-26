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
