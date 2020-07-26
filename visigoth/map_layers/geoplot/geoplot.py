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


import os
import os.path
import math

from visigoth.svg import text
from visigoth.map_layers import MapLayer
from visigoth.utils.js import Js

from .multiline import Multiline
from .multipoint import Multipoint
from .multipolygon import Multipolygon

class Geoplot(MapLayer):

    """
    Create a geo plot containing specified multi-points or multi-lines or multi-polygons

    Keyword Arguments:
        multipoints(list): points list of Multipoint
        multilines(list): lines list of Multiline
        multipolys(list): polygons to plot list of Multipoylgon
        font_height(int) : font size in pixels for labels
        text_attributes(dict): a dict containing SVG name/value attributes to apply to labels
        label_fill(str): fill colour for displaying labels 

    Notes:
        The following JavaScript events are dispatched from this element:

        channel select_id: for points/lines/polygons with an assigned id, dispatch the id value when clicked
        channel select_category: for points/lines/polygons with an assigned category, dispatch the category value when clicked
    """

    def __init__(self, multipoints=[], multilines=[], multipolys=[],font_height=12,text_attributes={}, label_fill="#FFFFFF80"):
        super(Geoplot, self).__init__()
        self.multipoints = multipoints
        self.multilines = multilines
        self.multipolys = multipolys
        self.font_height = font_height
        self.text_attributes = text_attributes
        self.label_fill = label_fill

        self.width = None
        self.height = None
        self.boundaries = None
        self.x_axis_max = None
        self.x_axis_min = None
        self.y_axis_max = None
        self.y_axis_min = None
        self.scale  = None
        self.projection = None

        self.popups = []
        self.popup_map = {}
        self.group_properties = {}
        self.group_labels = {}
        self.label_ids = set()
        self.circles = {}
        self.markers = {}
        self.points = {}
        self.lines = {}
        self.polygons = {}    
        self.labels = {} 
        self.popup_groups = {}

    def add(self,multithing):
        if isinstance(multithing,Multipoint):
            self.multipoints.append(multithing)
        elif isinstance(multithing,Multiline):
            self.multilines.append(multithing)
        elif isinstance(multithing,Multipolygon):
            self.multipolys.append(multithing)
        else:
            raise Exception("Object is not a Multithing")

    def clear(self):
        self.multipoints = []
        self.multipolys = []
        self.multilines = []

    def configureLayer(self,ownermap,width,height,boundaries,projection,zoom_to,fmt):
        super().configureLayer(ownermap,width,height,boundaries,projection,zoom_to,fmt)
        (self.min_lon,self.min_lat) = boundaries[0]
        (self.max_lon,self.max_lat) = boundaries[1]

    def isSearchable(self):
        return True

    def trackBoundaries(self,point):
        (lon,lat) = point
        if self.min_lon == None or lon < self.min_lon:
            self.min_lon = lon
        if self.min_lat == None or lat < self.min_lat:
            self.min_lat = lat
        if self.max_lon == None or lon > self.max_lon:
            self.max_lon = lon
        if self.max_lat == None or lat > self.max_lat:
            self.max_lat = lat

    def getBoundaries(self):
        self.min_lat = None
        self.min_lon = None
        self.max_lat = None
        self.max_lon = None

        for mp in self.multipoints:
            for point in mp.getCoordinates():
                self.trackBoundaries(point)
        for ml in self.multilines:
            for line_coords in ml.getCoordinates():
                for point in line_coords:
                    self.trackBoundaries(point)
        for mp in self.multipolys:
            for poly in mp.getCoordinates():
                for ring in poly:
                    for point in ring:
                        self.trackBoundaries(point)

        return ((self.min_lon,self.min_lat),(self.max_lon,self.max_lat))

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def inarea(self,lonlat):
        (lon,lat) = lonlat
        return lon >= self.min_lon and lon <= self.max_lon and lat >= self.min_lat and lat <= self.max_lat

    def drawTo(self,cx,cy):
        super().drawTo(cx,cy)

    def transform(self,point,ox,oy):
        return self.getXYFromLonLat(point)
        # (x,y) = self.projection.fromLonLat(point)
        # return (self.scale*(x - self.x_axis_min)+ox,oy+self.height-self.scale*(y - self.y_axis_min))

    def centroid(self,points):
        mean_x = sum([x for (x,_) in points])/len(points)
        mean_y = sum([y for (_,y) in points])/len(points)
        return (mean_x,mean_y)

    def max(self,points):
        max_x = max([x for (x,_) in points])
        max_y = max([y for (_,y) in points])
        return (max_x,max_y)

    def bbox_area(self,points):
        min_x = min([x for (x,_) in points])
        max_x = max([x for (x,_) in points])
        min_y = min([y for (_,y) in points])
        max_y = max([y for (_,y) in points])
        return (max_x-min_x)*(max_y-min_y)
        
    def simplify(self,points):
        simp = []
        simp.append(points[0])
        for p in points[1:]:
            if int(p[0]) != int(simp[-1][0]) or int(p[1]) != int(simp[-1][1]):
                simp.append(p)
        return simp

    def getLineCenter(self,tps):
        # find the longest line segment and return its center point and angle in radians
        l_max_length = None
        l_max = None
        for pidx in range(len(tps)-1):
            (x1,y1) = tps[pidx]
            (x2,y2) = tps[pidx+1]
            l = math.sqrt((x1-x2)**2 + (y1-y2)**2)
            if not l_max or l > l_max_length:
                l_max_length = l
                l_max = [ (x1,y1),(x2,y2)]
        (x1,y1) = l_max[0]
        (x2,y2) = l_max[1]
        x = x1 + (x2-x1)/2
        y = y1 + (y2-y1)/2
        angle=math.atan2(y2-y1,x2-x1)
        return (x,y,angle)

    def getLineLength(self,tps):
        length = 0
        for pidx in range(len(tps)-1):
            (x1,y1) = tps[pidx]
            (x2,y2) = tps[pidx+1]
            length += math.sqrt((x1-x2)**2 + (y1-y2)**2)
        return length

    def build(self,fmt):
        super().build(fmt)
        if self.boundaries:
            (self.x_axis_min,self.y_axis_min) = self.projection.fromLonLat(self.boundaries[0])
            (self.x_axis_max,self.y_axis_max) = self.projection.fromLonLat(self.boundaries[1])
            self.scale = self.width/(self.x_axis_max-self.x_axis_min)

    def addPopup(self,title,trigger_ids,popup,x,y):
        self.popups.append((title,trigger_ids,popup,x,y))

    def drawPopups(self,doc):
        for (title,trigger_ids,popup,x,y) in self.popups:
            for trigger_id in trigger_ids:
                self.popup_map[trigger_id] = popup.getId()
            popup.build(doc.getFormat())
            oy = y
            y -= 20+popup.getHeight()/2
            doc.getDiagram().connect(self,"toggle",popup,"toggle")
            pg = doc.openGroup(popup=True)
            popup.draw(doc,x,y)
            doc.closeGroup()
            self.popup_groups[pg.getId()] = { "x":x, "y":oy }

    def drawPoints(self,doc,cx,cy,ox,oy):

        for idx in range(len(self.multipoints)):
            mp = self.multipoints[idx]
            points = mp.getCoordinates()
            label = mp.getLabel()
            mpid = mp.getId()
            category = mp.getCategory()
            popup = mp.getPopup()
            props = mp.getProperties()

            doc.openGroup().addAttr("class","geopoint").addAttr("tabindex","0")

            tpoints = []
            pids = []
            for pidx in range(len(points)):
                point = points[pidx]
                if self.inarea(point):
                    tp = self.transform(point,ox,oy)
                    tpoints.append(tp)
                    pid = mp.draw(doc,tp)
                    if mp.getMarker():
                        self.markers[pid] = {"x":tp[0],"y":tp[1]}
                    else:
                        self.circles[pid] = {"r":mp.getRadius(),"sw":mp.getStrokeWidth()}
                    self.points[pid] = {}
                    if mpid:
                        self.points[pid]["id"] = mpid
                    if category:
                        self.points[pid]["category"] = category
                
                    pids.append(pid)
            if label:
                (clon,clat) = self.centroid(points)
                (mlon,mlat) = self.max(points)
                tp = self.transform((clon,mlat),ox,oy)
                self.addPointLabel(tp,mp.getRadius(),mp.getMarker(),label,doc)

            group_id = doc.closeGroup().getId()
            if popup and tpoints:
                (px,py) = self.centroid(tpoints)
                self.addPopup(label,pids,popup,px,py)
            self.group_properties[group_id] = props
            self.group_labels[group_id] = label

    def addPointLabel(self,tp,radius,marker,label,doc):
        label_y = tp[1]
        label_y -= 2*radius
        label_x = tp[0] + radius
        g = doc.openGroup()
        t = text(label_x,label_y,label,font_height=self.font_height,text_attributes=self.text_attributes,fill=self.label_fill)
        t.setVerticalCenter()
        t.setHorizontalCenter()
        self.label_ids.add(g.getId())
        doc.add(t)
        doc.closeGroup()
        self.labels[g.getId()] = {"x":tp[0], "y":tp[1]}

    def drawLines(self,doc,cx,cy,ox,oy):

        for idx in range(len(self.multilines)):
            mp = self.multilines[idx]
            lines = mp.getCoordinates()
            label = mp.getLabel()
            mpid = mp.getId()
            category = mp.getCategory()
            
            popup = mp.getPopup()
            props = mp.getProperties()
            
            doc.openGroup().addAttr("class","geopath").addAttr("tabindex","0")

            longest_len = 0
            longest_tps = None
            lids = []

            for lidx in range(len(lines)):
                line = lines[lidx]
                include = False
                for point in line:
                    if self.inarea(point):
                        include = True

                if include:
                    tps = [self.transform(point,ox,oy) for point in line]
                    if longest_tps == None or longest_len < self.getLineLength(tps):
                        longest_tps = tps
                    ls = mp.draw(doc,tps)
                    if label:
                        self.addLineLabel(tps,label,doc)
                    for (l,sw) in ls:
                        lid = l.getId()
                        self.lines[lid] = { "sw":sw }
                        if mpid:
                            self.lines[lid]["id"] = mpid
                        if category:
                            self.lines[lid]["category"] = category

                        lids.append(lid)
            group_id = doc.closeGroup().getId()
            if popup:
                (x,y,_) = self.getLineCenter(longest_tps)
                self.addPopup(label,lids,popup,x,y)
            self.group_properties[group_id] = props
            self.group_labels[group_id] = label

    def addLineLabel(self,tps,label,doc):
        (label_x,label_y,angle) = self.getLineCenter(tps)
        g = doc.openGroup()
        t = text(label_x,label_y,label,font_height=self.font_height,text_attributes=self.text_attributes,fill=self.label_fill)
        t.setVerticalCenter()
        t.setHorizontalCenter()
        t.setRotation(angle)
        self.label_ids.add(g.getId())
        doc.add(t)
        doc.closeGroup()
        self.labels[g.getId()] = {"x":label_x, "y":label_y}
        

    def drawPolygons(self,doc,cx,cy,ox,oy):

        for idx in range(len(self.multipolys)):

            mp = self.multipolys[idx]
            mpid = mp.getId()
            category = mp.getCategory()
            polys = mp.getCoordinates()
            label = mp.getLabel()
            
            popup = mp.getPopup()
            props = mp.getProperties()
            
            doc.openGroup().addAttr("class","geopolygon").addAttr("tabindex","0")

            largest_area = 0
            largest_poly = None
            pids = []

            for pidx in range(len(polys)):
                include = False

                poly = polys[pidx]
                for ring in poly:
                    for point in ring:
                        if self.inarea(point):
                            include = True
                if include:
                    plotrings = [self.simplify([self.transform(point,ox,oy) for point in ring]) for ring in poly]
                    p = mp.draw(doc,plotrings)
                    if largest_poly == None or self.bbox_area(plotrings[0]) > largest_area:
                        largest_poly = plotrings[0]
                    if label:
                        self.addPolygonLabel(plotrings,label,doc)
                    pid = p.getId()
                    self.polygons[pid] = { "sw":mp.getStrokeWidth() }
                    if mpid:
                        self.polygons[pid]["id"] = mpid
                    if category:
                        self.polygons[pid]["category"] = category
                    pids.append(pid)

            group_id = doc.closeGroup().getId()
            if popup:
                (px,py) = self.centroid(largest_poly)
                self.addPopup(label,pids,popup,px,py)

            self.group_properties[group_id] = props
            self.group_labels[group_id] = label

    def addPolygonLabel(self,polyrings,label,doc):
        # find the centroid
        polypoints = polyrings[0]
        (cx,cy) = self.centroid(polypoints)
        g = doc.openGroup()
        t = text(cx,cy,label,font_height=self.font_height,text_attributes=self.text_attributes,fill=self.label_fill)
        t.setVerticalCenter()
        t.setHorizontalCenter()
        self.label_ids.add(g.getId())
        doc.add(t)
        doc.closeGroup()
        self.labels[g.getId()] = {"x":cx, "y":cy}


    def draw(self,doc,cx,cy,constructJs=True):
        ox = cx - self.width/2
        oy = cy - self.height/2

        self.drawPolygons(doc,cx,cy,ox,oy)
        self.drawLines(doc,cx,cy,ox,oy)
        self.drawPoints(doc,cx,cy,ox,oy)
     
        self.drawPopups(doc)

        config = {
            "popup_map": self.popup_map, 
            "label_ids":list(self.label_ids), 
            "group_properties":self.group_properties, 
            "group_labels":self.group_labels,
            "circles":self.circles,
            "markers":self.markers,
            "points":self.points,
            "lines":self.lines,
            "polygons":self.polygons,
            "labels":self.labels,
            "popups":self.popup_groups }

        with open(os.path.join(os.path.split(__file__)[0], "geoplot.js"), "r") as jsfile:
            jscode = jsfile.read()
            Js.registerJs(doc,self,jscode,"geoplot",cx,cy,config,constructJs)
        return config
