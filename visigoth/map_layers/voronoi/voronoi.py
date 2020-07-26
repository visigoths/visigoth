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
import os.path

from visigoth.svg import circle,polygon
from visigoth.map_layers import MapLayer
from visigoth.utils.mapping import Mapping
from visigoth.utils.js import Js
from visigoth.map_layers.voronoi.bowyer_watson import circumcircle, bowyer_watson

from visigoth.utils.colour import DiscretePalette, ContinuousPalette
from visigoth.utils.marker import MarkerManager

from visigoth.utils.data import Dataset

class Voronoi(MapLayer):
    """
    Create a Voronoi plot

    Args:
        data (list): A relational data set (for example, list of dicts/lists/tuples describing each row)

    Keyword Args:
        lat (str or int): Identify the column to provide the latitude value for each point
        lon (str or int): Identify the column to provide the longitude value for each point
        colour (str or int): Identify the column to provide the colour for each point
        label (str or int): Identify the column to provide the label for each point
        size (str or int): Identify the column to provide the size for each point
        stroke (str): stroke color for plotting boundaries
        stroke_width (int): stroke width for plotting boundaries
        palette(object) : a ContinuousPalette or DiscretePalette instance to control chart colour
        marker_manager(object) : a MarkerManager instance to control marker appearance
    """
    def __init__(self,data,lat=0,lon=1,colour=2,label=None,size=None,stroke="black",stroke_width=2,palette=None,marker_manager=None):
        super(Voronoi, self).__init__()
        self.width = 0
        self.height = 0
        self.projection = None
        self.stroke = stroke
        self.stroke_width = stroke_width
        self.colour = colour

        self.min_x = None
        self.min_y = None
        self.max_x = None
        self.max_y = None
        self.boundaries = None
        self.scale_x = None
        self.scale_y = None
        self.polygons = []
        self.dataset = Dataset(data)
        self.input_data = self.dataset.query([lon,lat,colour,label,size])

        if not palette:
            if not self.colour or self.dataset.isDiscrete(self.colour):
                palette = DiscretePalette()
            else:
                palette = ContinuousPalette()
        self.setPalette(palette)

        if not marker_manager:
            marker_manager = MarkerManager()
            marker_manager.setDefaultRadius(15)
        self.setMarkerManager(marker_manager)

        for (_,_,colour,_,size) in self.input_data:
            self.getMarkerManager().noteSize(size)
            self.getPalette().getColour(colour)



    def getBoundaries(self):
        if not self.boundaries:
            self.boundaries = Mapping.getBoundingBox([(lon,lat) for (lon,lat,_,_,_) in self.input_data],0.05)
        return self.boundaries

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

    def build(self,fmt):
        super().build(fmt)
        self.data = []
        for (lon,lat,col,label,size) in self.input_data:
            prj = self.projection.fromLonLat((lon,lat))
            self.data.append((prj[0],prj[1],col,label,size))

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
        self.data.append((self.max_data_x + self.x_data_range*1.1,self.max_data_y + self.y_data_range,None,"",0))
        self.data.append((self.min_data_x - self.x_data_range,self.max_data_y + self.y_data_range,None,"",0))
        self.data.append((self.max_data_x + self.x_data_range,self.min_data_y - self.y_data_range,None,"",0))
        self.data.append((self.min_data_x - self.x_data_range,self.min_data_y - self.y_data_range,None,"",0))

        points=[(x,y) for (x,y,_,_,_) in self.data]
        delaunay = bowyer_watson(points)

        for (x,y,col,label,size) in self.data:
            triangles = [triangle for triangle in delaunay if (x,y) in list(triangle)]
            polygon_points = self.dual(triangles,(x,y))
            self.polygons.append((polygon_points,col,label))

    def draw(self,doc,cx,cy):      
        ox = cx - self.width/2
        oy = cy - self.height/2

        for (ppoints,col,label) in self.polygons:
            if col is not None:
                col = self.getPalette().getColour(col)
            else:
                col = "white" # colour so-called edge regions white
            kwargs={}
            if label:
                kwargs["tooltip"] = str(label)
            p = polygon(map(lambda p: self.transform(ox,oy,p[0],p[1]),ppoints),col,self.stroke,self.stroke_width,**kwargs)
            doc.add(p)

        for (x,y,col,label,size) in self.data:
            col = self.getPalette().getColour(col)
            (px,py) = self.transform(ox,oy,x,y)
            kwargs={}
            if label:
                kwargs["tooltip"] = str(label)
            c = circle(px,py,self.getMarkerManager().getRadius(size),col,**kwargs)
            c.addAttr("stroke",self.stroke)
            c.addAttr("stroke-width",self.stroke_width)
            doc.add(c)

        doc.closeGroup()
        with open(os.path.join(os.path.split(__file__)[0],"voronoi.js"),"r") as jsfile:
            jscode = jsfile.read()
        config = {}
        Js.registerJs(doc,self,jscode,"voronoi",cx,cy,config)