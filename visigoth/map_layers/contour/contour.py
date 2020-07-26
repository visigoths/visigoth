
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
from urllib import request
import os
import os.path

from visigoth.common import DiagramElement
from visigoth.common.image import Image
from visigoth.utils.mapping import Mapping
from visigoth.svg import circle, path, rectangle, text, polygon
from visigoth.map_layers import MapLayer
from visigoth.utils.mapping import Projections
from visigoth.utils.js import Js

class Contour(MapLayer):
    """
    Create a Contour plot

    Keyword Arguments:
        data (list): list of rows, where each row is an equal size list of column values values
        contour_interval (float): gap between contours
        label_fn(function): function to compute a str contour label from a numeric threshold
        stroke(str) : the colour to use for contour lines
        stroke_width(float) : the width (in pixels) to use for contour lines
        font_height(int) : font size in pixels for contour labels
        text_attributes(dict): a dict containing SVG name/value attributes to apply to contour labels
    """
    def __init__(self,data=[],contour_interval=10,label_fn=lambda x:"%d"%(x),stroke="brown",stroke_width=1,font_height=8,text_attributes={}):
        super(Contour, self).__init__()
        self.data = data
        self.width = None
        self.height = None
        self.rows = len(self.data)
        self.columns = 0
        if self.data:
            self.columns = len(self.data[0])
            if self.columns == 0:
                raise Exception(Contour.INPUT_DATA_FORMAT_ERROR)
        for row in self.data:
            if len(row) != self.columns:
                raise Exception(Contour.INPUT_DATA_FORMAT_ERROR)
        self.contour_interval = contour_interval
        if self.contour_interval <= 0.0:
            raise Exception(Contour.CONTOUR_INTERVAL_ERROR)
        self.projection = None
        self.max_val = 1
        self.min_val = 0
        if self.data:
            self.max_val = max([v for rowdata in self.data for v in rowdata])
            self.min_val = min([v for rowdata in self.data for v in rowdata])
        self.stroke = stroke
        self.label_fn = label_fn
        self.stroke_width = stroke_width
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.clip = True
        self.boundaries = None

    CONTOUR_INTERVAL_ERROR = "contour_interval parameter must be a positive number > 0"
    INPUT_DATA_FORMAT_ERROR = "data parameter must be a non-empty list of equally sized non-empty lists containing elevation values"

    def getBoundaries(self):
        if self.boundaries:
            return self.boundaries
        return ((0,0),(1,self.rows/self.columns))

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to,fmt):
        self.width = width
        self.height = height
        self.ownermap = ownermap
        self.boundaries = boundaries
        self.projection = projection
        if self.boundaries == None:
            self.boundaries = ((0,0),(self.columns-1,self.rows-1))
            self.projection = Projections.EPSG_4326

    def computeCellIndex(self,tdata,cell_x,cell_y):
        sw = tdata[cell_y+1][cell_x]
        nw = tdata[cell_y][cell_x]
        ne = tdata[cell_y][cell_x+1]
        se = tdata[cell_y+1][cell_x+1]
        index = sw | (se << 1) | (ne << 2) | (nw << 3)
        return index

    def computeCellLine(self,index,cell_x,cell_y):
        scale = 1
        nw_x = cell_x-1
        nw_y = cell_y-1
        if index == 0 or index == 15:
            return []
        if index == 1 or index == 14:
            return [(nw_x,nw_y+scale/2,nw_x+scale/2,nw_y+scale)]
        if index == 2 or index == 13:
            return [(nw_x+scale/2,nw_y+scale,nw_x+scale,nw_y+scale/2)]
        if index == 3 or index == 12:
            return [(nw_x,nw_y+scale/2,nw_x+scale,nw_y+scale/2)]
        if index == 4 or index == 11:
            return [(nw_x+scale/2,nw_y,nw_x+scale,nw_y+scale/2)]
        if index == 5:
            return [(nw_x,nw_y+scale/2,nw_x+scale/2,nw_y),(nw_x+scale/2,nw_y+scale,nw_x+scale,nw_y+scale/2)]
        if index == 6 or index == 9:
            return [(nw_x+scale/2,nw_y,nw_x+scale/2,nw_y+scale)]
        if index == 7 or index == 8:
            return [(nw_x,nw_y+scale/2,nw_x+scale/2,nw_y)]
        if index == 10:
            return [(nw_x,nw_y+scale/2,nw_x+scale/2,nw_y+scale),(nw_x+scale/2,nw_y,nw_x+scale,nw_y+scale/2)]
        return []

    def reposition(self,path,ox,oy):
        rpath = []
        (lonmin,latmin) = self.sw
        (lonmax,latmax) = self.ne

        (emin,nmin) = self.projection.fromLonLat(self.sw)
        (emax,nmax) = self.projection.fromLonLat(self.ne)

        self.scalex = self.width / (emax-emin)
        self.scaley = self.height / (nmax-nmin)

        for (x,y) in path:
            lon = lonmin + (x / (self.columns-1)) * (lonmax-lonmin)
            lat = latmax - (y / (self.rows-1)) * (latmax-latmin)
            (e,n) = self.projection.fromLonLat((lon,lat))
            rpath.append((ox+(e-emin)*self.scalex,oy+self.height - (n-nmin)*self.scaley))
        return rpath

    def distance(self,p0,p1):
        return math.sqrt((p0[0]-p1[0])**2 + (p0[1]-p1[1])**2)

    def stitch(self,lines):
        fragmentsByStart = {}
        fragmentsByEnd = {}
        rings = []

        for (x1,y1,x2,y2) in lines:
            p1 = (x1,y1)
            p2 = (x2,y2)
            if p1 in fragmentsByStart:
                ring = fragmentsByStart[p1]
                ring.insert(0,p2)
                del fragmentsByStart[p1]
                fragmentsByStart[p2] = ring
            elif p1 in fragmentsByEnd:
                ring = fragmentsByEnd[p1]
                ring.append(p2)
                del fragmentsByEnd[p1]
                fragmentsByEnd[p2] = ring
            elif p2 in fragmentsByStart:
                ring = fragmentsByStart[p2]
                ring.insert(0,p1)
                del fragmentsByStart[p2]
                fragmentsByStart[p1] = ring
            elif p2 in fragmentsByEnd:
                ring = fragmentsByEnd[p2]
                ring.append(p1)
                del fragmentsByEnd[p2]
                fragmentsByEnd[p1] = ring
            else:
                ring = [p1,p2]
                fragmentsByStart[p1] = ring
                fragmentsByEnd[p2] = ring
                rings.append(ring)

        incomplete = rings[:]

        def prepend(l1,l2):
            l2.reverse()
            for i in l2:
                l1.insert(0,i)

        total = []
    
        for ring in rings:
            if ring in incomplete:
                assembling = True
                while assembling:
                    assembling = False
                    for other in incomplete:
                        if other != ring:
                            if ring[-1] == other[0]:
                                incomplete.remove(other)
                                ring += other[1:]
                            elif other[-1] == ring[0]:
                                incomplete.remove(other)
                                prepend(ring,other[:-1])
                            elif ring[0] == other[0]:
                                incomplete.remove(other)
                                other.reverse()
                                prepend(ring,other[:-1])
                            elif ring[-1] == other[-1]:
                                incomplete.remove(other)
                                other.reverse()
                                ring += other[1:]
                            else:
                                continue
                            assembling = True
                            break
                if ring[0] == ring[-1]:
                    total.append(ring)
                else:
                    raise Exception("Unable to compute closed contour")
        return total

    def isConcave(self,points,tdata):
        # find left most line centre (left_cx,left_cy)
        left_cx = None
        left_cy = None
        for idx in range(0,len(points)):
            (px1,py1) = points[idx]
            (px2,py2) = points[(idx + 1) % len(points)]
            cx = (px1+px2)/2
            cy = (py1+py2)/2 
            if left_cx == None or cx < left_cx:
                left_cx = cx
                left_cy = cy
        # for the cell this center falls in, try and infer if the cell is concave
        cell_x = math.floor(left_cx)
        cell_y = math.floor(left_cy)
        nw = tdata[cell_y][cell_x]
        sw = tdata[cell_y+1][cell_x]
        ne = tdata[cell_y][cell_x+1]
        se = tdata[cell_y+1][cell_x+1]
        return (nw == 1 and sw ==1) or ((ne==0 or se==0) and (nw==1 or sw==1))

    def interpolate(self,path,threshold):
        ipath = []
        for (x,y) in path:
            y0 = int(y)
            x0 = int(x)
            y1 = int(y+1)
            x1 = int(x+1)

            if y1 >= self.rows or y0 >= self.rows:
                ipath.append((x,y))
                continue
            if x1 >= self.columns or x0 >= self.columns:
                ipath.append((x,y))
                continue

            if x == x0:
                v0 = self.data[y0][x0]
                v1 = self.data[y1][x0]
                if v1 != v0:
                    y = y0 + (threshold-v0)/(v1-v0)

            elif y == y0:
                v0 = self.data[y0][x0]
                v1 = self.data[y0][x1]
                if v1 != v0:
                    x = x0 + (threshold-v0)/(v1-v0)

            ipath.append((x,y))
        return ipath

    def simplify(self,path):
        simplified = []
        for point in path:
            if simplified == [] or self.distance(point,simplified[-1]) > 0.1:
                simplified.append(point)
        return simplified

    def computeContourLines(self,threshold,ox,oy):
        lines = []
        tdata = []
        def binarize(x):
            if x < threshold:
                return 0
            else:
                return 1

        tdata.append([0]*(self.columns+2))
        for rowdata in self.data:
            trowdata = [binarize(val) for val in rowdata]
            tdata.append([0]+trowdata+[0])
        tdata.append([0]*(self.columns+2))

        for cell_y in range(self.rows+1):
            for cell_x in range(self.columns+1):
                index = self.computeCellIndex(tdata,cell_x,cell_y)
                cellLines = self.computeCellLine(index,cell_x,cell_y)
                for cellLine in cellLines:
                    lines.append(cellLine)

        total = self.stitch(lines)
        
        interpolated_total = [self.interpolate(path,threshold) for path in total]

        concavity = [self.isConcave(points,tdata) for points in interpolated_total]
        
        repositioned_total = [self.reposition(path,ox,oy) for path in interpolated_total]

        simplified_total = [self.simplify(path) for path in repositioned_total]

        return (simplified_total,concavity)

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def build(self,fmt):
        self.sw = self.boundaries[0]
        self.ne = self.boundaries[1]
        super().build(fmt)

    def setPalette(self,palette):
        super().setPalette(palette)
        palette.getColour(self.min_val)
        palette.getColour(self.max_val)

    def generateLabel(self,points,threshold):

        def lineProperties(p0,p1):
            lX = p1[0] - p0[0]
            lY = p1[1] - p0[1]
            mX = p0[0] + (p1[0]-p0[0])*0.5
            mY = p0[1] + (p1[1]-p0[1])*0.5
            return (math.sqrt(lX**2 + lY**2),math.atan2(lY, lX),(mX,mY))

        maxl = None
        angle = None
        coords = None

        for idx in range(1,len(points)):
            p0 = points[idx-1]
            p1 = points[idx]
            (l,a,mp) = lineProperties(p0,p1)

            if maxl == None or l > maxl:
                maxl = l
                coords = mp
                angle = a

        t = text(coords[0],coords[1],self.label_fn(threshold))
        t.setRotation(angle)
        t.addAttr("stroke",self.stroke)
        if self.text_attributes:
            t.addAttrs(self.text_attributes)
        t.addAttr("font-size",self.font_height)
        t.addAttr("text-anchor", "middle")
        t.addAttr("dominant-baseline", "middle")
        return t

    def draw(self,doc,cx,cy):
        ox = cx - self.width/2
        oy = cy - self.height/2

        if self.clip:
            self.openClip(doc,cx,cy)

        contourTotal = []
        threshold = self.contour_interval * (self.min_val//self.contour_interval)

        while threshold < self.min_val:
            if self.palette:
                r = rectangle(ox,oy,self.getWidth(),self.getHeight(),fill=self.palette.getColour(threshold))
                doc.add(r)
            threshold += self.contour_interval


        while threshold < self.max_val:
            (total,concavity) = self.computeContourLines(threshold,ox,oy)
            contourTotal.append((threshold,total,concavity))
            threshold += self.contour_interval


        if self.palette:
            for (threshold,contours,concavity) in contourTotal:
                for idx in range(len(contours)):
                    cl = contours[idx]
                    isconcave = concavity[idx]
                    if len(cl) > 1:
                        fill = None
                        area_threshold = threshold
                        if isconcave:
                            area_threshold = threshold-self.contour_interval
                        fill = self.palette.getColour(area_threshold)
                        p = path(cl,None,0,smoothing=0.5,closed=True,fill=fill,tooltip=str(area_threshold))
                        doc.add(p)

        if self.stroke_width:
            for (threshold,contours,_) in contourTotal:
                for cl in contours:
                    if len(cl) > 1:
                        p = path(cl,self.stroke,self.stroke_width,smoothing=0.5,closed=True,fill=None)
                        doc.add(p)
                        if self.label_fn:
                            doc.add(self.generateLabel(cl,threshold))

        if self.clip:
            self.closeClip(doc)

        with open(os.path.join(os.path.split(__file__)[0],"contour.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc,self,jscode,"contour",cx,cy,config)
        