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


from visigoth.svg import hexagon,circle,text
from math import radians,sin,cos,pi


class HexGrid(object):

    def __init__(self,width,gridwidth,gridheight,max_distance,fill,stroke,stroke_width,dimension,dimensionPalette,instance_radius):
        self.width = width
        self.gx = gridwidth
        self.gy = gridheight

        self.max_distance = max_distance
        self.distances = {}
        self.model = None

        self.rangle = radians(30)
        self.dlength = self.width/((2*cos(self.rangle)*(0.5+self.gx)))

        self.off_lg = self.dlength * cos(self.rangle)
        self.off_sm = self.dlength * sin(self.rangle)

        self.fill = fill
        self.stroke = stroke
        self.stroke_width = stroke_width

        for d in range(0,self.max_distance+1):
            for xc in range(0,self.gx):
                for yc in range(0,self.gy):
                    self.genDistance(xc,yc,xc,yc,0,d)

        self.element_class_map = {}

        self.dimension = dimension
        self.dimensionPalette = dimensionPalette
        self.instance_radius = instance_radius
        if self.instance_radius == None:
            self.instance_radius = self.dlength*0.1

    def getElementClassMap(self):
        return self.element_class_map

    def setModel(self,model):
        self.model = model

    def position(self,xc,yc,xd,yd):
        pos = str(xc) + "."
        pos += str(yc) + "."
        pos += str(xd) + "."
        pos += str(yd)
        return pos

    def putDistance(self,xc,yc,xd,yd,d):
        self.distances[self.position(xc,yc,xd,yd)] = d

    def getDistance(self,xc,yc,xd,yd):
        key = self.position(xc,yc,xd,yd)
        if key in self.distances:
            return self.distances[key]
        else:
            return None

    def neighbours(self,x,y):
        n_list = []
        n_list.append(((x-1) % self.gx,y))
        n_list.append(((x+1) % self.gx,y))
        n_list.append((x, (y+1) % self.gy))
        n_list.append((x, (y-1) % self.gy))
        if x % 2 == 0:
            n_list.append(((x-1) % self.gx,(y+1) % self.gy))
            n_list.append(((x-1) % self.gx,(y-1) % self.gy))
        else:
            n_list.append(((x+1) % self.gx,(y+1) % self.gy))
            n_list.append(((x+1) % self.gx,(y-1) % self.gy))
        return n_list

    def genDistance(self,xc,yc,xd,yd,r,d):
        if r == d:
            if self.getDistance(xc,yc,xd,yd) == None:
                self.putDistance(xc,yc,xd,yd,r)
        else:
            n_list = self.neighbours(xd,yd)
            for (nx,ny) in n_list:
                self.genDistance(xc,yc,nx,ny,r+1,d)

    def build(self,fmt):
        if self.dimensionPalette:
            dvals = [self.model.getDimensionValue(self.dimension,xc,yc) for xc in range(0,self.gx) for yc in range(0,self.gy)]
            minVal = min(dvals)
            maxVal = max(dvals)
            self.dimensionPalette.getColour(minVal)
            self.dimensionPalette.getColour(maxVal)

    def hexacenter(self,origin,x,y):
        (ox,oy) = origin
        rangle = radians(30)
        off_sm = self.dlength*sin(rangle)
        off_lg = self.dlength*cos(rangle)
        yc = oy + (float(y)*(self.dlength+off_sm))+(0.5*float(self.dlength))+off_sm
        xc = ox + ((float(x)+0.5)*(2*off_lg))
        if y % 2 == 1:
            xc += off_lg
        return (xc,yc)

    def inHexagon(self,px,py,hx,hy):
        s = self.dlength
        x = abs(px - hx)
        y = abs(py - hy)
        return x < 3**0.5 * min(s - y, s / 2)

    def findHexagon(self,coords):
        (px,py) = coords
        for xc in range(0,self.gx):
            for yc in range(0,self.gy):
                (hx,hy) = self.hexacenter((0,0),xc,yc)
                if self.inHexagon(px,py,hx,hy):
                    return (xc,yc)
        return None

    def renderGrid(self,diagram,ox,oy,scores,catmap):
        rangle = radians(30)
        off_sm = self.dlength*sin(rangle)
        off_lg = self.dlength*cos(rangle)
        hx = ox
        labels = []

        for xc in range(0,self.gx):
            for yc in range(0,self.gy):

                (x,y) = self.hexacenter((ox,oy),xc,yc)

                fill = self.fill
                if self.dimension != None:
                    fill = self.dimensionPalette.getColour(self.model.getDimensionValue(self.dimension,xc,yc))
                poly = hexagon(x, y, self.dlength, fill, self.stroke, self.stroke_width)
                cls = str(xc)+"_"+str(yc)
                self.element_class_map[poly.getId()] = cls
                diagram.add(poly)

                assigned = scores[(xc,yc)]
                if assigned:
                    cx = x
                    cy = y

                    r2 = self.dlength * 0.7 - self.instance_radius
                    r3 = r2+(self.instance_radius*1.5)

                    assigned = sorted(assigned,key=lambda x: x[1])
                    theta = 0
                    step = pi*2 / len(assigned)
                    if step > 1.0:
                        step = 1.0

                    for (label,colour,category) in assigned:
                        if category and category not in catmap:
                            catmap[category] = []
                        if not colour:
                            colour = self.fill
                        px = cx+r2*cos(theta)
                        py = cy+r2*sin(theta)
                        pxl = cx+r3*cos(theta)
                        pyl = cy+r3*sin(theta)
                        c = circle(px,py,self.instance_radius,colour,label)
                        if category:
                            catmap[category].append(c.getId())
                        t = text(pxl,pyl,label)
                        t.addAttr("dominant-baseline","middle")
                        t.addAttr("paint-order","stroke")
                        t.addAttr("fill",colour)
                        t.addAttr("stroke-width", "10px")
                        t.addAttr("stroke", "white")
                        if theta > pi/2 and theta < pi*1.5:
                            t.addAttr("text-anchor","end")
                            t.setRotation(theta-pi)
                        else:
                            t.addAttr("text-anchor","start")
                            t.setRotation(theta)
                        t.addAttr("visibility","hidden")
                        t.addAttr("class",cls)
                        diagram.add(c)
                        labels.append(t)
                        theta += step

        for label in labels:
            diagram.add(label)
        return (ox+off_lg+self.gx*(2*off_lg)+10,oy+off_sm+(self.gy)*(self.dlength+off_sm)+10)
