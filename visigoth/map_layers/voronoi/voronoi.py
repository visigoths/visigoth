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
import os.path

from visigoth.common import DiagramElement
from visigoth.svg import circle,polygon
from visigoth.map_layers import MapLayer
from visigoth.utils.mapping import Mapping
from visigoth.utils.js import Js
from visigoth.map_layers.voronoi.bowyer_watson import circumcircle, bowyer_watson

class Voronoi(MapLayer):
    """
    Create a Voronoi plot

    Args:
        data (list): (x,y,col,label) tuples for each point

    Keyword Args:
        stroke (str): stroke color for plotting boundaries
        stroke_width (int): stroke width for plotting boundaries
        radius (int): radius for plotting region centers (set to 0 to omit)
    """
    def __init__(self,data,stroke="black",stroke_width=2,radius=5):
        super(Voronoi, self).__init__()
        self.width = 0
        self.height = 0
        self.projection = None
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.radius = radius
        self.min_x = None
        self.min_y = None
        self.max_x = None
        self.max_y = None
        self.boundaries = None
        self.scale_x = None
        self.scale_y = None
        self.polygons = []
        self.input_data = data
        self.data = []

    def getBoundaries(self):
        if not self.boundaries:
            self.boundaries = Mapping.getBoundingBox([(lon,lat) for (lon,lat,_,_) in self.input_data],0.05)
        return self.boundaries

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to):
        self.ownermap = ownermap
        self.width = width
        self.height = height
        self.boundaries = boundaries
        self.projection = projection

    def getHeight(self):
        return self.height

    def getWidth(self):
        return self.width

    def transform(self,ox,oy,x,y):
        px = ox + (x - self.min_x)*self.scale
        py = oy + (self.max_y-y)*self.scale
        return (px,py)

    def distance(self,c1,c2):
        return math.sqrt((c1[0]-c2[0])**2)+((c1[1]-c2[1])**2)

    def computeMinR(self):
        t = [(d,self.transform(0,0,d[0],d[1])) for d in self.data]
        for (d,dc) in t:
            self.min_r[d] = min([self.distance(dc,dc2) for (d2,dc2) in t if d != d2])/2

    def dual(self,triangles,center):
        (x,y) = center
        def triangle_bisector(triangle):
            ((ax,ay),(bx,by),(cx,cy)) = triangle
            (ux,uy,_) = circumcircle(ax,ay,bx,by,cx,cy)
            return (ux,uy)
        points = map(triangle_bisector,triangles)
        points_and_angle = map(lambda p:(math.atan2(p[0]-x,p[1]-y),p),points)
        return [(p[1][0],p[1][1]) for p in sorted(points_and_angle,key=lambda x:x[0])]

    def build(self):
        self.data = []
        for (lon,lat,col,label) in self.input_data:
            prj = self.projection.fromLonLat((lon,lat))
            self.data.append((prj[0],prj[1],col,label))

        self.min_data_x = min([p[0] for p in self.data])
        self.max_data_x = max([p[0] for p in self.data])
        self.min_data_y = min([p[1] for p in self.data])
        self.max_data_y = max([p[1] for p in self.data])

        (self.min_x,self.min_y) = self.projection.fromLonLat(self.boundaries[0])
        (self.max_x,self.max_y) = self.projection.fromLonLat(self.boundaries[1])
        
        self.x_range = self.max_x - self.min_x
        self.y_range = self.max_y - self.min_y

        self.x_data_range = self.max_data_x - self.min_data_x
        self.y_data_range = self.max_data_y - self.min_data_y

        self.scale = self.width/self.x_range
        self.height = self.scale * self.y_range

        # add extreme points at each corner to create regions at the edge of the diagram
        self.data.append((self.max_data_x + self.x_data_range*1.1,self.max_data_y + self.y_data_range,"white",""))
        self.data.append((self.min_data_x - self.x_data_range,self.max_data_y + self.y_data_range,"white",""))
        self.data.append((self.max_data_x + self.x_data_range,self.min_data_y - self.y_data_range,"white",""))
        self.data.append((self.min_data_x - self.x_data_range,self.min_data_y - self.y_data_range,"white",""))

        points=[(x,y) for (x,y,_,_) in self.data]
        delaunay = bowyer_watson(points)

        for (x,y,col,label) in self.data:
            triangles = [triangle for triangle in delaunay if (x,y) in list(triangle)]
            polygon_points = self.dual(triangles,(x,y))
            self.polygons.append((polygon_points,col,label))

    def draw(self,doc,cx,cy):      
        ox = cx - self.width/2
        oy = cy - self.height/2

        for (ppoints,col,label) in self.polygons:
            kwargs={}
            if label:
                kwargs["tooltip"] = label
            p = polygon(map(lambda p: self.transform(ox,oy,p[0],p[1]),ppoints),col,self.stroke,self.stroke_width,**kwargs)
            doc.add(p)

        if self.radius:
            for (x,y,col,label) in self.data:
                (px,py) = self.transform(ox,oy,x,y)
                kwargs={}
                if label:
                    kwargs["tooltip"] = label
                c = circle(px,py,self.radius,col,**kwargs)
                c.addAttr("stroke",self.stroke)
                c.addAttr("stroke-width",self.stroke_width)
                doc.add(c)

        doc.closeGroup()
        with open(os.path.join(os.path.split(__file__)[0],"voronoi.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc,self,jscode,"voronoi",cx,cy,config)